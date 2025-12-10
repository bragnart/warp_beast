# src/gui/components/dialog/msg_sender.py
import flet as ft
from typing import Optional
from pydantic import BaseModel, Field

class MsgSenderTheme(BaseModel):
    width: int = Field(550)
    height:int = Field(100)
    input_font: str = Field("arsenal")
    input_txtsize: int = Field(16)
    input_bgcolor: str = Field("#7F85C4")
    input_color: str = Field("#CD12BD")
    input_bordercolor: str = Field("#ABF15A")
    input_borderradius: int = Field(15)
    btn_icon: str = Field("send")


class MsgSender(ft.Stack):

    def __init__(
            self,
            theme: Optional[MsgSenderTheme] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if theme is None:
            theme = MsgSenderTheme()
        self.width = theme.width
        self.height = theme.height

        self.input = ft.TextField(
            multiline=True,
            shift_enter=True,
            autofocus=True,
            expand=True,
            text_style=ft.TextStyle(
                size=theme.input_txtsize,
                font_family=theme.input_font,
                color=theme.input_color
            ),
            bgcolor=theme.input_bgcolor,
            border_color=theme.input_bordercolor,
            border_radius=ft.border_radius.all(theme.input_borderradius),
            on_submit=self._send,
        )

        self.send_btn = ft.IconButton(
            icon=theme.btn_icon,
            right=0,
            top=0,
            on_click=self._send,
            opacity=0.5,
        )
        
        self.controls.append(self.input)
        self.controls.append(self.send_btn)



    async def _send(self, e):
        msg_txt = self.input.value
        self.input.value = ""
        self.update()
        self.parent._send(msg_txt)

