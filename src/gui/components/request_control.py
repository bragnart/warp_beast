# src/gui/components/request_control.py
import flet as ft
from ..app_context import AppContext

class RequestControl(ft.Container):

    def __init__(self, app_context: AppContext, **kwargs):
        super().__init__(**kwargs)
        self.app_context = app_context
        self.width = 550
        self.height = 300
        #self.bgcolor = ft.Colors.BLACK45
        self.border_radius = ft.border_radius.all(10)
        #self.blur = 5
        self.gradient = ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[
                ft.Colors.random(),
                ft.Colors.BLUE_ACCENT_200
            ]
        )
        self.padding = 10
        self.shadow = ft.BoxShadow(
            color=ft.Colors.BLACK54,
            blur_radius=10,
            offset=ft.Offset(0, 4)
        )

        self.response_display = ft.Markdown(
            value="**Ответ будет здесь...**",
            selectable=False,
            extension_set=ft.MarkdownExtensionSet.GITHUB_FLAVORED,
            code_theme=ft.MarkdownCodeTheme.MONOKAI_SUBLIME,
            width=530,
            height=200,
            )
        self.request_input = ft.TextField(
            label="Введите запрос",
            label_style=ft.TextStyle(color=ft.Colors.WHITE70),
            width=530,
            bgcolor=ft.Colors.BLACK26,
            color=ft.Colors.WHITE,
            on_submit=self._on_send
        )
        self.column = ft.Column(
            expand=True,
            controls=[
                self.response_display,
                self.request_input
            ]
        )
        self.content = self.column


    async def _on_send(self, e):
        usr_input = self.request_input.value
        self.request_input.value = ""
        self.request_input.update()
        
        ai_session = self.app_context.ai_session
        response = await ai_session.request_model(usr_input)
        self.response_display.value = response.text
        self.response_display.update()