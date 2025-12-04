# src/ai/tools/memory_tools.py
from __future__ import annotations

from typing import List, Optional, Any, Dict

from pydantic import BaseModel, Field
from pydantic_ai import Tool, RunContext, FunctionToolset

from ..deps import SessionDeps


class MemorySearchInput(BaseModel):
    """Входные данные для инструмента поиска воспоминаний."""
    queries: List[str] = Field(
        ...,
        description=(
            "Список коротких текстовых запросов для поиска по памяти. "
            "Обычно это 1–3 строки, описывающие текущую тему или вопрос."
        ),
    )

    limit: int = Field(
        5,
        ge=1,
        le=20,
        description="Максимальное количество результатов на один запрос.",
    )


def memory_search_func(ctx: RunContext[SessionDeps], input: MemorySearchInput) -> str:
    """
    Инструмент для поиска релевантных воспоминаний в Mem0.

    Ожидает, что в ctx.deps.session есть:
      - mem_client: клиент Mem0 (MemoryClient или совместимый),
      - необязательно user_id: идентификатор пользователя.

    Возвращает человекочитаемый список найденных воспоминаний,
    пригодный для прямого подмешивания в контекст.
    """
    session = ctx.deps.agent_session

    mem_client = session.mem0_client.client

    # Выбираем user_id: явный из инпута или из сессии, если есть
    uid = session.user_id

    all_results: List[Dict[str, Any]] = []

    for q in input.queries:
        if not q.strip():
            continue

        # Вызов search у Mem0: сигнатура ориентирована на hosted API. [web:180][web:202]
        try:
            res = mem_client.search(
                query=q,
                user_id=uid,
                filters={"agent_id": session.id},
                limit=input.limit,
            )
        except Exception as e:
            return f"Ошибка при обращении к памяти: {e!s}"

        # SDK может вернуть dict с ключом "results" или сразу список. [web:180][web:212]
        if isinstance(res, dict):
            res_list = res.get("results", []) or []
        else:
            res_list = res or []

        all_results.extend(res_list)

    if not all_results:
        return "Подходящих воспоминаний не найдено."

    # Дедуп по id и приведение к тексту
    seen_ids = set()
    memories: List[str] = []

    for item in all_results:
        if not isinstance(item, dict):
            memories.append(str(item))
            continue

        mid = item.get("id")
        if mid and mid in seen_ids:
            continue
        if mid:
            seen_ids.add(mid)

        text = (
            item.get("memory")
            or item.get("text")
            or item.get("content")
            or str(item)
        )
        memories.append(text)

    if not memories:
        return "Подходящих воспоминаний не найдено."

    lines = [f"{i+1}) {m}" for i, m in enumerate(memories)]
    return "Найденные воспоминания:\n" + "\n".join(lines)


MemorySearchTool = Tool(
    function=memory_search_func,
    name="MemorySearchTool",
    description=(
        "Инструмент для поиска релевантных воспоминаний в долговременной памяти. "
        "Используй его, когда нужно вспомнить прошлые факты, идеи, проекты или контекст "
        "по текущей теме разговора."
    ),
)

MemoryToolset = FunctionToolset(
    tools=[
        MemorySearchTool,
    ],
    id="MemoryToolset",
)
