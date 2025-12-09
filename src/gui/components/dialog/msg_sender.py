# src/gui/components/msg_sender.py
import flet as ft


class MsgSender(ft.Container):

    def __init__(
            self,
            width: int,
            height: int,
            txt_input_bgcolor: str,
            txt_input_color: str,
            txt_input_font: str,
            txt_input_bordercolor: str,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.width = width
        self.height = height

        self.txt_input = ft.TextField(
            keyboard_type=ft.KeyboardType.MULTILINE,
            multiline=True,
            autofocus=True,
            bgcolor=txt_input_bgcolor,
            text_style=ft.TextStyle(
                font_family=txt_input_font,
                color=txt_input_color,
            ),
            border_radius=ft.border_radius.all(17),
            border_color=txt_input_bordercolor,
            shift_enter=True,
            on_submit=self._send,
        )


        self.content = self.txt_input



    async def _send(self, e):
        msg_txt = self.txt_input.value
        self.txt_input.value = ""
        await self.page.data["send_msg_txt"](msg_txt)
        self.update()
