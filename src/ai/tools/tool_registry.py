# src/ai/tools/tool_registry.py
from dataclasses import dataclass
from pydantic_ai import WrapperToolset, RunContext, ToolsetTool
from typing import Any, Dict
from ..deps import SessionDeps

@dataclass
class ToolRegistry(WrapperToolset):
    """
    Реестр инструментов сессии.
    """

    async def call_tool(
        self,
        name: str,
        tool_args: Dict[str, Any],
        ctx: RunContext[SessionDeps],
        tool: ToolsetTool
    ):  


        try:
            
            ctx.deps.agent_session.log.info(f"Применяется инструмент {name} с аргументами {tool_args}")
            result = await super().call_tool(name, tool_args, ctx, tool)
            ctx.deps.agent_session.log.success(f"Инструмент {name} успешно применен: {result}")
            return result
        except Exception as e:
            ctx.deps.agent_session.log.error(f"При применении {name} произошла ошибка: {str(e)}")
            return str(e)