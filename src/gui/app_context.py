# src/gui/app_context.py
import flet as ft
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from ..ai.config import AIConfig
from ..ai.agent_session import AgentSession

class AppContext(BaseModel):
    #cfg: ConfigDict = ConfigDict(arbitrary_types_allowed=True)
    ai_config: AIConfig = Field(default_factory=lambda: AIConfig())
    _ai_session: Optional[AgentSession] = None
    _page: Optional[ft.Page] = None


    @property
    def ai_session(self) -> AgentSession:
        if self._ai_session is None:
            self._ai_session = self.create_session()
        return self._ai_session
    
    @property
    def page(self) -> ft.Page:
        return self._page

    def create_session(self):
        self._ai_session = AgentSession(config=self.ai_config)
        return self._ai_session