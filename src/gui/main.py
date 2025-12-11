# src/gui/main.py
from __future__ import annotations
import flet as ft
import asyncio

from typing import Optional
from pathlib import Path

from src.ai import AgentSession, AIConfig

from .constants import ASSETS_PATH, FONT_DICT

from .components.settings_view import SettingsView, SettingsViewTheme
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



    page.data["ai_config"] = None


    page.data["session"] = None

    def init_session(ai_config: AIConfig):
        page.data["ai_config"] = ai_config
        page.data["session"] = AgentSession(config=ai_config)

        page.update()

    def start_session(ai_config: AIConfig):
        init_session(ai_config)
        settings_view.visible = False
        chat_view.visible = True
        page.update()

    def on_keyboard_event(e: ft.KeyboardEvent):
        if e.key == "Escape":
            page.window.close()
        if e.key == "Q" and e.ctrl:
            page.window.close()
        if e.key == "S" and e.ctrl:
            settings_view.visible = True
            page.go("settings_view")

    

    page.on_keyboard_event = on_keyboard_event


    chat_view_theme = ChatViewTheme()
    settings_view_theme = SettingsViewTheme()

    page.data["themes"]["chat_view"] = chat_view_theme
    page.data["themes"]["settings_view"] = settings_view_theme

    chat_view = ChatView(theme=page.data["themes"]["chat_view"])
    chat_view.visible = False
    settings_view = SettingsView(theme=page.data["themes"]["settings_view"], on_start_callback=start_session)

    page.views.append(chat_view)
    page.views.append(settings_view)
    

    page.go("settings_view")

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