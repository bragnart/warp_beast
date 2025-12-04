# src/ai/agent_session.py
from __future__ import annotations

import os
import sys
import asyncio
from pathlib import Path
from typing import Type, List, Any, TypeVar, Optional

import logfire
from pydantic import BaseModel
from pydantic_core import to_jsonable_python
from pydantic_ai import Agent, RunContext, AbstractToolset, ModelMessagesTypeAdapter, ModelRequest, ModelResponse, BinaryContent
from pydantic_ai.messages import ModelMessage, UserPromptPart, SystemPromptPart, FilePart, BinaryImage
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

if __name__ == '__main__':
    from rich import print
    cfg = AIConfig(model_name="qwen/qwen3-vl-30b-a3b-thinking", enable_mem0=False, reasoning=True)
    session = AgentSession(config=cfg)
    async def main():
        response = await session.request_model("Что на картинке этой?", img_file=Path("C:\\Users\\Xiaomi\\Downloads\\generated-image - 2025-12-03T211201.176.png"))
        print(response)
        print("Ответ модели:", response.text)
        print("Мысля модели:", response.thinking)
    asyncio.run(main())