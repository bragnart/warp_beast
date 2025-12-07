# src/gui/components/dialog/base_message.py
import flet as ft
from pathlib import Path
from typing import Optional

COLORS = {
    "msgbox_bg": "#151616",
    "msgbox_lght": "#3d3e3e",
    "msgbox_dk": "#0d0d0d",
    
}

class Avatar(ft.Column):

    def __init__(
            self,
            role: str,
            image_path: str | Path,
            role_txt_color: str = "#BD5AA9",
            size: int = 50,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.role = role
        self.image_path = Path(image_path)
        self.role_txt_color = role_txt_color
        self.size = size
        self.width = size+15



        self.pic = ft.Image(
            src=str(self.image_path),
            width=self.size,
            height=self.size
        )
        self.role_txt = ft.Text(
            value=self.role.upper(),
            #text_align=ft.TextAlign.CENTER,
            color=self.role_txt_color,
            weight=ft.FontWeight.BOLD
        )
        self.controls = [
            self.pic,
            self.role_txt
        ]
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER


class MsgTextColumn(ft.Column):

    def __init__(
            self,
            msg_txt: str,
            thought_txt: Optional[str] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.msg_txt = msg_txt
        self.thought_txt = thought_txt


        self.msg_txt_mkdn = ft.Markdown(
            value=self.msg_txt,
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.COMMON_MARK,
            code_theme=ft.MarkdownCodeTheme.ATELIER_DUNE_DARK,
        )
        te = True if self.thought_txt is not None else False
        self.thought_txt_mkdn = ft.Markdown(
            value=self.thought_txt,
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.COMMON_MARK,
            code_theme=ft.MarkdownCodeTheme.ATELIER_DUNE_DARK,
            visible=False,
        )
        self.thought_txt_btn = ft.TextButton(
            text="Мысли агента",
            icon=ft.Icons.DATA_OBJECT,
            visible=te,
            on_click=self._th_click,
        )
        self.scroll = ft.ScrollMode.AUTO
        self.expand = True
        self.controls = [
            self.thought_txt_mkdn,
            self.thought_txt_btn,
            self.msg_txt_mkdn
        ]


    def _th_click(self, e):
        self.thought_txt_mkdn.visible = not self.thought_txt_mkdn.visible
        self.thought_txt_mkdn.update()


class MsgContainer(ft.Container):

    def __init__(
            self,
            width: int,
            height: int,
            avatar_size: int,
            msg_txt: str,
            thought_txt: Optional[str] = None,
            role: str = "agent",
            **kwargs
    ):
        super().__init__(**kwargs)
        self.width = width
        self.height = height
        self.border_radius = ft.border_radius.all(17)

        if role =="agent":
            av_img = Path("src/assets/agent_avatar.png")
        else:
            av_img = Path("src/assets/user_avatar.png")
        
        self.avatar = Avatar(
            role=role,
            image_path=av_img,
            size=avatar_size
        )
        self.txtmsgcolumn = MsgTextColumn(
            msg_txt=msg_txt,
            thought_txt=thought_txt
        )

        self.content = ft.Row(
            controls=[
                self.avatar,
                self.txtmsgcolumn
            ],

        )
        

# class BaseMessageDialog(ft.Container):

#     def __init__(
#             self,
#             role: str,
#             avatar_imgpath: str,
#             message_text: str,
#             thinking_text: Optional[str] = None,
#            background_color: str = "#151616",
#             textcontrol_color: str = "#4286c1",
#             message_font: str = "gothra",
#             width: int = 600,
#             height: int = 200,
#             **kwargs
#     ):
#         super().__init__(**kwargs)
#         self.role = role
#         self.avatar_imgpath = avatar_imgpath
#         self.message_text = message_text
#         self.thnkngbtn_visible = False
#         self.thinking_text = thinking_text
#         if thinking_text is not None:
#             self.thnkngbtn_visible = True
#         self.background_color = background_color
#         self.textcontrol_color = textcontrol_color
#         self.message_font = message_font

        
#         self.width = width
#         self.height = height
#         self.padding = 10
#         self.margin = ft.margin.all(10)
#         self.bgcolor = self.background_color
#         self.border_radius = ft.border_radius.all(17)
#         self.shadow = [
#             ft.BoxShadow(
#                 offset=ft.Offset(27, 27),
#                 blur_radius=30,
#                 blur_style=ft.ShadowBlurStyle.NORMAL,
#                 color="#5c9f8c"
#             ),
#             ft.BoxShadow(
#                 offset=ft.Offset(-27, -27),
#                 blur_radius=30,
#                 blur_style=ft.ShadowBlurStyle.NORMAL,
#                 color="#9aead8"
#             )
#         ]



#         self.avatar = ft.Column(
#             controls=[
#                 ft.CircleAvatar(
#                     radius=40,
#                     foreground_image_src=self.avatar_imgpath,
#                 ),
#                 ft.Text(
#                     self.role.capitalize(),
#                     color=ft.Colors.PURPLE_ACCENT_100,
#                     size=16,
#                 )
#             ]
#         )

#         self.msgtxt = ft.Markdown(
#             value=self.message_text,
#             selectable=False,
#             extension_set=ft.MarkdownExtensionSet.GITHUB_FLAVORED,
#             code_theme=ft.MarkdownCodeTheme.MAGULA,
#             )

#         self.thnkngtxt = ft.Markdown(
#             value=self.thinking_text if self.thinking_text else "Thinking...",
#             selectable=False,
#             extension_set=ft.MarkdownExtensionSet.GITHUB_FLAVORED,
#             code_theme=ft.MarkdownCodeTheme.MAGULA,
#             visible=False
#             )
        
#         self.thnkngbtn = ft.TextButton(
#             text="Мысли ИИ-агента",
#             icon=ft.Icons.POLICY,
#             on_click=self._on_thinking_click,
#             visible=self.thnkngbtn_visible
#         )

#         self.msgclmn = ft.Column(
#             controls=[self.msgtxt, self.thnkngtxt, self.thnkngbtn],
#             alignment=ft.MainAxisAlignment.CENTER,
#             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#             expand=True,
#             scroll=ft.ScrollMode.AUTO,
#         )

#         self.content = ft.Row(
#             controls=[
#                 self.avatar,
#                 self.msgclmn
#             ],
#             alignment=ft.MainAxisAlignment.START,
#             vertical_alignment=ft.CrossAxisAlignment.CENTER,
#             expand=True
#         )

#     def _on_thinking_click(self, e: ft.ControlEvent):
#         self.thnkngtxt.visible = not self.thnkngtxt.visible
#         self.thnkngtxt.update()



if __name__ == '__main__':
#     TXT="""
#     ```python
#     # src/gui/components/dialog/base_message.py
#     import flet as ft

#     from typing import Optional

#     ```
#     """
#     THT = "Это мысли ИИ-агента, которые можно показать или скрыть по нажатию кнопки. **Это пример диалогового окна с аватаром, сообщением и кнопкой для отображения мыслей агента.**"*10
    
    def main(page: ft.Page):
        page.window.icon = "icon.ico"
        page.fonts = {
            "gothra": "https://github.com/bragnart/warp_beast/blob/dialog_windows/src/assets/fonts/gothra.ttf",
        }
        page.theme_mode = ft.ThemeMode.DARK
        cnt = MsgContainer(
            width=500,
            height=200,
            avatar_size=50,
            msg_txt="Ну что, поговорили?"
        )
        page.add(cnt)
        

    ft.app(target=main, assets_dir="D:\\myworks\\agents\\warp_beast\\src\\assets")