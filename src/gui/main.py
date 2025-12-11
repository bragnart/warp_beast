# src/gui/main.py
from __future__ import annotations
import flet as ft
import asyncio

from typing import Optional
from pathlib import Path

from src.ai import AgentSession, AIConfig

from .constants import ASSETS_PATH, FONT_DICT

from .components.dialog import ChatView, ChatViewTheme, MsgContainer, MsgContainerTheme


def main(page: ft.Page):
    page.window.width = 560
    page.window.height = 800
    page.window.bgcolor = ft.Colors.TRANSPARENT
    page.window.icon = "icon.ico"
    page.window.center()
    page.theme_mode = ft.ThemeMode.DARK
    page.fonts = FONT_DICT


    page.data = {
        "themes": {},
        "funcs": {},
        "session": None,
    }

    ai_config = AIConfig(model_name="x-ai/grok-4.1-fast", enable_mem0=False)

    page.data["ai_config"] = ai_config

    session = AgentSession(config=ai_config)
    page.data["session"] = session

    def on_keyboard_event(e: ft.KeyboardEvent):
        if e.key == "Escape":
            page.window.close()
        if e.key == "Q" and e.ctrl:
            page.window.close()


    page.on_keyboard_event = on_keyboard_event

    chat_view_theme = ChatViewTheme()

    page.data["themes"]["chat_view"] = chat_view_theme

    chat_view = ChatView(theme=page.data["themes"]["chat_view"])
    
    page.views.append(chat_view)

    page.go("chat_view")

    async def send_msg(msg_txt: str, image_path: Optional[Path] = None):
        session: AgentSession = page.data["session"]
        response = await session.run(
            user_msg=msg_txt,
            image_path=image_path  # Уже поддерживается!
        )
        chat_view._receive(response)

    page.data["funcs"]["send_msg"] = send_msg

if __name__ == '__main__':
    ft.app(target=main, assets_dir=str(ASSETS_PATH))