# src/ai/agent_session.py
from __future__ import annotations

import os
import sys
import asyncio
from pathlib import Path
from typing import Type, List, Any, TypeVar, Optional, Union

import logfire
from pydantic import BaseModel
from pydantic_core import to_jsonable_python
from pydantic_ai import Agent, RunContext, AbstractToolset, ModelMessagesTypeAdapter, ModelRequest, ModelResponse, BinaryContent
from pydantic_ai.messages import ModelMessage, UserPromptPart, SystemPromptPart, FilePart, BinaryImage, UserContent, ImageUrl
from pydantic_ai.direct import model_request
from pydantic_ai.models.openrouter import OpenRouterModel, OpenRouterModelSettings, OpenRouterProviderConfig, OpenRouterReasoning
from pydantic_ai.providers.openrouter import OpenRouterProvider

from loguru import logger
from shortuuid import uuid
from dotenv import load_dotenv

from .config import AIConfig
from .mem0_client import Mem0aiClient
from .deps import SessionDeps
from .output_models import ResponseModel, TandT
from .tools import ToolRegistry, MemoryToolset, lc_fm_toolset, search_toolset

logfire.configure()
logfire.instrument_pydantic_ai()
logfire.instrument_httpx(capture_all=True)


T = TypeVar("T", bound=ResponseModel)
DEFAULT_TOOLSETS = [MemoryToolset, lc_fm_toolset, search_toolset]


def set_logger(logfile: Path):
    """Настраивает логгер для сессии агента."""
    logger.remove()
    logger.add(logfile, rotation="10 MB", retention="7 days", compression="zip")
    logger.add(
        sys.stderr,
        format="<fg #6495ED>{time:YYYY-MM-DD HH:mm:ss}</fg #6495ED> | <level>{level}</level> | <fg #FFCB99>{module}</fg #FFCB99>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
        colorize=True,
        enqueue=True,
    )
    logger.level("INFO", color="<fg #55ECC9>", icon="💡")
    logger.level("DEBUG", color="<fg #8888FF>", icon="🐛")
    logger.level("ERROR", color="<fg #F64444>", icon="❌")
    logger.level("WARNING", color="<fg #FFAA00>", icon="⚠️")
    logger.level("SUCCESS", color="<fg #03C57E>", icon="✅")
    return logger

def build_model(
    model_name: str,
    temperature: float,
    max_tokens: int = 8000,
    reasoning: bool = False,
    timeout: float = 30.0,
) -> OpenRouterModel:
    """Создает и настраивает модель OpenRouter."""
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    provider = OpenRouterProvider(api_key=api_key)
    settings = OpenRouterModelSettings(
        openrouter_reasoning=OpenRouterReasoning(
            enabled=reasoning,
            effort="high" if reasoning else None,
            ),
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=timeout,
        parallel_tool_calls=False,
        
    )
    # Можно добавить extra_body для специфичных параметров OpenRouter, если нужно
    return OpenRouterModel(model_name=model_name, settings=settings, provider=provider)


class AgentSession:

    def __init__(
            self,
            config: AIConfig,
            run_id: Optional[str] = None,
            saves_dir: str | Path = "saves",
            project_id: Optional[str] = None,
    ):
        self.cfg = config
        self.run_id = run_id or uuid()
        self.project_id = project_id
        self.saves_dir = Path(saves_dir)
        self.dir = self.saves_dir / self.cfg.agent_id
        self.dir.mkdir(parents=True, exist_ok=True)
        self.logfile = self.dir / ".log"
        self.log = set_logger(self.logfile)
        if self.cfg.enable_mem0:
            self._init_mem0_memory()
        self._init_runner()
        self.deps = SessionDeps(agent_session=self)
        self.toolsets = []
        self.history = []
        self._init_toolsets()
        self.log.success(f"Сессия агента {self.cfg.agent_id} инициализирована с run_id {self.run_id}.")

    def _init_toolsets(self):
        self.toolsets = []
        for toolset in DEFAULT_TOOLSETS:
            self.toolsets.append(ToolRegistry(toolset))

        self.log.info(f"Инициализированы инструменты: {[ts.wrapped.id for ts in self.toolsets]}")

    def _init_mem0_memory(self):
        self.mem0_client = Mem0aiClient(
            project_id=self.project_id,
            user_id=self.cfg.user_id,
            agent_id=self.cfg.agent_id,
            run_id=self.run_id
        )
        self.log.info("Mem0 клиент инициализирован.")

    def _init_runner(self):

        load_dotenv()

        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            self.log.error("Не найден OPENROUTER_API_KEY в переменных окружения")
            raise EnvironmentError("Не найден OPENROUTER_API_KEY в переменных окружения")
        self.model = build_model(
            model_name=self.cfg.model_name,
            temperature=self.cfg.temperature,
            max_tokens=self.cfg.max_tokens,
            reasoning=self.cfg.reasoning,
            timeout=self.cfg.timeout
        )
        self.runner = Agent(
            model=self.model,
            system_prompt=self.cfg.system_prompt,
            deps_type=SessionDeps,
            retries=3,
        )
        self.log.info(f"Модель {self.cfg.model_name} и агент инициализированы.")
    
    async def request_model(self, user_message: str, system_prompt: str = "Ты ассистент", instruction: str = "Ответь пользователю", img_file: Optional[Path] = None) -> ModelResponse:
        """Отправляет запрос модели и возвращает ответ."""
        self.log.info(f"Отправка запроса модели: {user_message}")

        parts=[
            SystemPromptPart(content=system_prompt),
            UserPromptPart(content=user_message),
        ]
        if img_file and img_file.exists():
            parts.append(
                UserPromptPart(content=[BinaryContent.from_path(img_file)])
            )
            self.log.info(f"Добавлено изображение к запросу: {img_file.name}")
        response = await model_request(
            model=self.model,

            messages=[ModelRequest(
                parts=parts,
                instructions=instruction,
                run_id=self.run_id,
            )]
        )
        self.log.info(f"Получен ответ модели: {response}")
        return response
    
    async def run(
            self,
            user_msg: str,
            instruction: Optional[str] = None,
            image_path: Optional[Union[str, Path]] = None,
    ):
        if instruction is None:
            instruction = self.cfg.run_instruction
        
        if image_path:
            import mimetypes
            image_path = Path(image_path)
            image_bytes = image_path.read_bytes()
            image_media_type, _ = mimetypes.guess_type(image_path)
            user_msg = [
                user_msg,
                BinaryContent(image_bytes, media_type=image_media_type)
            ]
            self.log.info(f"Добавлено изображение {str(image_path)} с типом {image_media_type}")
            #Потом добавить кастомные ошибки и их обработку

        result = await self.runner.run(
            user_prompt=user_msg,
            message_history=self.history,
            instructions=instruction,
        )
        self.history.extend(result.new_messages())
        return result


if __name__ == '__main__':
    from rich import print
    cfg = AIConfig(model_name="qwen/qwen3-vl-30b-a3b-thinking", enable_mem0=False, reasoning=True)
    session = AgentSession(config=cfg)
    async def main():
        response = await session.run("Привет, меня зовут Егор. О себе немного поведай.")
        print(response)
        print("Ответ модели:", response.output)
        print("Мысля модели:", response.response.thinking)
        response = await session.run("Не забыл как меня зовут? Скажи мое имя. И скажи что на картинке изображено.", image_path="src/assets/user_avatar.png")
        print(response)
        print("Ответ модели:", response.output)
        print("Мысля модели:", response.response.thinking)
    asyncio.run(main())