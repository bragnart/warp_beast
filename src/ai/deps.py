# src/ai/deps.py
from __future__ import annotations
import pendulum
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .agent_session import AgentSession

@dataclass
class SessionDeps:

    agent_session: AgentSession

    def get_context_info(self):
        s = []
        s.append("Контекст текущего запроса:")
        t = pendulum.now().format("YYYY-MM-DD HH:mm:ss")
        s.append(f"Время: {t}")
        s.append(f"Твой ID: {self.agent_session.cfg.agent_id}")
        s.append(f"Пользовательский ID: {self.agent_session.cfg.user_id}")
        return "\n".join(s)