# src/gui/components/config_control.py
import flet as ft
from ..app_context import AppContext
from ...ai.config import AIConfig, DEFAULT_SYSTEM_PROMPT

class ConfigControl(ft.Container):

    def __init__(self, app_context: AppContext,  **kwargs):
        super().__init__(**kwargs)
        self.app_context = app_context
        self.width = 550
        self.height = 700
        self.bgcolor = ft.Colors.BLUE_GREY_200
        self.padding = 10
        self.border_radius = 10
        self.shadow = ft.BoxShadow(
            color=ft.Colors.BLACK54,
            blur_radius=10,
            offset=ft.Offset(0, 4)
        )

        self.agent_id_input = ft.TextField(label="Agent ID", width=530, value="WarpBeast", bgcolor=ft.Colors.BLUE_GREY_300, color=ft.Colors.RED_300)
        self.user_id_input = ft.TextField(label="User ID", width=530, value="Gantz", bgcolor=ft.Colors.BLUE_GREY_300, color=ft.Colors.PINK_ACCENT)
        self.model_name_input = ft.TextField(label="Model Name", width=530, value="qwen/qwen3-vl-30b-a3b-thinking", bgcolor=ft.Colors.BLUE_GREY_300)
        self.temperature_input = ft.TextField(label="Temperature", value="0.7", bgcolor=ft.Colors.BLUE_GREY_300, width=110)
        self.max_tokens_input = ft.TextField(label="Max Tokens", value="8000", bgcolor=ft.Colors.BLUE_GREY_300, width=130)
        self.reasoning_input = ft.Chip(label=ft.Text("Reasoning"), selected=True, bgcolor=ft.Colors.BLUE_GREY_300, width=130, on_click=self._toggle_reasoning)
        self.mem0_input = ft.Chip(label=ft.Text("Mem0"), selected=True, bgcolor=ft.Colors.BLUE_GREY_300, width=130, on_click=self._toggle_mem0)
        self.system_prompt_input = ft.TextField(label="System Prompt", width=530, height=400, multiline=True, bgcolor=ft.Colors.BLUE_GREY_300, value=DEFAULT_SYSTEM_PROMPT)
        self.accept_button = ft.IconButton(icon=ft.Icons.CHECK, on_click=self._on_accept)
        self.column = ft.Column(
            expand=True,
            controls=[
                self.agent_id_input,
                self.user_id_input,
                self.model_name_input,
                ft.Row(controls=[
                    self.temperature_input,
                    self.max_tokens_input,
                    self.reasoning_input,
                    self.mem0_input
                ],
                width=530,
                ),
                self.system_prompt_input,
                ft.Row(controls=[
                    self.accept_button], alignment=ft.MainAxisAlignment.END)
            ]
        )

        self.content = self.column

    def _toggle_reasoning(self, e):
        self.reasoning_input.selected = not self.reasoning_input.selected
        self.reasoning_input.update()

    def _toggle_mem0(self, e):
        self.mem0_input.selected = not self.mem0_input.selected
        self.mem0_input.update()


    def get_config(self) -> AIConfig:
        cfg = AIConfig(
            agent_id=self.agent_id_input.value,
            user_id=self.user_id_input.value,
            model_name=self.model_name_input.value,
            temperature=float(self.temperature_input.value),
            max_tokens=int(self.max_tokens_input.value),
            reasoning=self.reasoning_input.selected,
            enable_mem0=self.mem0_input.selected,
            system_prompt=self.system_prompt_input.value
        )
        return cfg
    
    def _on_accept(self, e):
        cfg = self.get_config()
        self.app_context.ai_config = cfg
        self.app_context.create_session()
        self.disabled = True
        self.visible = False
        self.app_context.page.window.height = 305
        self.app_context.page.window.center()
        self.update()