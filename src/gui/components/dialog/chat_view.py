# src/gui/components/dialog/chat_view.py
import flet as ft
from typing import List, Optional, Literal
from pydantic import BaseModel, Field


from .base_message import ChatContainer, MsgContainer, ChatContainerTheme, MsgContainerTheme
from .msg_sender import MsgSender, MsgSenderTheme

class GradientBg(BaseModel):
    start: Literal["top left", "top right", "bottom left", "bottom right"] = Field("top left", description="Начало градиента")
    end: Literal["top left", "top right", "bottom left", "bottom right"] = Field("bottom right", description="Конец градиента")
    colors: List[str] = Field([ft.Colors.CYAN_300, ft.Colors.DEEP_PURPLE_300], description="Цвета градиента")

    @classmethod
    def from_dict(cls, data: dict):
        return cls.model_validate(data)
    
    def to_gradient(self):
        d = {
            "top left": ft.alignment.top_left,
            "top right": ft.alignment.top_right,
            "bottom left": ft.alignment.bottom_left,
            "bottom right": ft.alignment.bottom_right,
        }
        return ft.LinearGradient(
            colors=self.colors,
            begin=d[self.start],
            end=d[self.end],
        )

class ChatViewTheme(BaseModel):
    # width: int = Field(560)
    # height: int = Field(870)
    bgcolor: str = Field("#B654F4")
    gradient: dict | GradientBg = Field(default=GradientBg())
    chat_cnt_theme: ChatContainerTheme = Field(default=ChatContainerTheme())
    msg_cnt_theme: MsgContainerTheme = Field(default=MsgContainerTheme())
    msg_sender_theme: MsgSenderTheme = Field(default=MsgSenderTheme())



class ChatView(ft.View):

    def __init__(
            self,
            theme: Optional[ChatViewTheme] = None,
            **kwargs,
    ):

        super().__init__(**kwargs)
        if theme is None:
            theme = ChatViewTheme()
        
        self.route = "chat_view"
        self.bgcolor = theme.bgcolor

        self.theme = theme

        self.decoration = ft.BoxDecoration(
            gradient=self.theme.gradient.to_gradient(),
        )
        self.vertical_alignment = ft.VerticalAlignment.CENTER

        self.chat = ChatContainer(
            theme=self.theme.chat_cnt_theme
        )
        self.sender = MsgSender(
            theme=self.theme.msg_sender_theme
        )

        self.controls = [
            self.chat,
            self.sender,
        ]
        
    def _send(self, msg_txt):
        cnt = MsgContainer(
            role="user",
            msg_txt=msg_txt,
            theme=self.theme.msg_cnt_theme
        )
        self.chat.add_msg_container(cnt)
        self.update()
        func = self.page.data["funcs"]["send_msg"]
        self.page.run_task(func, msg_txt=msg_txt)

    def _receive(self, response):
        cnt = MsgContainer(
            role="agent",
            msg_txt=response.output,
            thought_txt=response.response.thinking,
            theme=self.theme.msg_cnt_theme
        )
        self.chat.add_msg_container(cnt)
        self.update()
        


