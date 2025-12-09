# src/gui/components/dialog/base_message.py
import flet as ft
from pathlib import Path
from typing import Optional

COLORS = {
    "msgbox_bg": "#151616",
    "msgbox_lght": "#3d3e3e",
    "msgbox_dk": "#0d0d0d",
    
}

def make_md_style(
        font: str, #шрифт для обычного текста, по умолчанию и к другим видам
        text_size: int, #размер текста
        main_text_color: str, #цвет основного обычного текста
        h_text_color: str, #цвет заголовков
        link_text_color: str, #цвет текста ссылок
        img_text_color: str, #цвет текста заменяющего картинку
        strong_text_color: str, #цвет жирного текста
        em_text_color: str, #курсива
        del_text_color: str, #зачеркнутого текста
        cd_text_color: str, #inline блоков кода
        bq_text_color: str, #цитат
        cb_text_color: str, #чекбоксов
        lb_text_color: str, # пунктов списков
        th_text_color: str, #заголовков таблицы
        tb_text_color: str, #пунктов таблицы
        cd_block_color: str, #цвет inline блока кода
        bq_block_color: str, #блока цитат
        tc_block_color: str, #ячейки таблицы
        line_color: str, # цвет линии (которая через ___ делается)
        cd_font: str = None, #шрифт кода инлайн
        bq_font: str = None, #шрифт цитат
):
    import copy
    cd_font = cd_font or font
    bq_font = bq_font or font
    main_text_style = ft.TextStyle(
        font_family=font,
        size=text_size,
        color=main_text_color
    )
    a_text_style = copy.deepcopy(main_text_style)
    a_text_style.color = link_text_color
    code_text_style = copy.deepcopy(main_text_style)
    code_text_style.font_family = cd_font
    code_text_style.color = cd_text_color
    em_text_style = copy.deepcopy(main_text_style)
    em_text_style.color = em_text_color
    em_text_style.italic = True
    strong_text_style = copy.deepcopy(main_text_style)
    strong_text_style.color = strong_text_color
    strong_text_style.weight = "bold"
    del_text_style = copy.deepcopy(main_text_style)
    del_text_style.color = del_text_color
    del_text_style.decoration = "line_through"
    bq_text_style = copy.deepcopy(main_text_style)
    bq_text_style.color = bq_text_color
    bq_text_style.font_family = bq_font
    img_text_style = copy.deepcopy(main_text_style)
    img_text_style.color = img_text_color
    img_text_style.italic = True
    cb_text_style = copy.deepcopy(main_text_style)
    cb_text_style.color = cb_text_color
    lb_text_style = copy.deepcopy(main_text_style)
    lb_text_style.color = lb_text_color
    th_text_style = copy.deepcopy(main_text_style)
    th_text_style.color = th_text_color
    th_text_style.weight = "bold"
    tb_text_style = copy.deepcopy(main_text_style)
    tb_text_style.color = tb_text_color
    h = []
    hsize = text_size

    for _ in range(6):
        s = copy.deepcopy(main_text_style)
        s.color = h_text_color
        s.size = hsize
        h.append(s)
        hsize += 3

    

    mds = ft.MarkdownStyleSheet(
        a_text_style=a_text_style,
        p_text_style=main_text_style,
        code_text_style=code_text_style,
        h1_text_style=h[5],
        h2_text_style=h[4],
        h3_text_style=h[3],
        h4_text_style=h[2],
        h5_text_style=h[1],
        h6_text_style=h[0],
        em_text_style=em_text_style,
        strong_text_style=strong_text_style,
        del_text_style=del_text_style,
        blockquote_text_style=bq_text_style,
        img_text_style=img_text_style,
        checkbox_text_style=cb_text_style,
        list_bullet_text_style=lb_text_style,
        table_head_text_style=th_text_style,
        table_body_text_style=tb_text_style,
        codeblock_decoration=ft.BoxDecoration(
            bgcolor=cd_block_color,
            border=ft.border.all(0.5, ft.Colors.AMBER)
        ),
        blockquote_decoration=ft.BoxDecoration(
            #bgcolor=bq_block_color,
            border=ft.border.all(0.5, ft.Colors.PINK),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[bq_block_color, ft.Colors.PINK_ACCENT]
            )
        ),
        table_cells_decoration=ft.BoxDecoration(
            bgcolor=ft.Colors.with_opacity(0.5, tc_block_color),
            border=ft.border.all(0.5, tc_block_color)
        ),
        horizontal_rule_decoration=ft.BoxDecoration(
            bgcolor=line_color
        )
    )
    return mds

dark_markdown_style = ft.MarkdownStyleSheet(


    # Основные стили текста
    p_text_style=ft.TextStyle(
        color=ft.Colors.GREY_100,
        size=14,
        font_family="gothra"
    ),
    
    # Заголовки (h1-h6) - светлые и крупные
    h1_text_style=ft.TextStyle(
        color=ft.Colors.WHITE,
        size=28,
        weight="bold",
        font_family="gothra"
    ),
    h2_text_style=ft.TextStyle(
        color=ft.Colors.GREY_50,
        size=24,
        weight="bold",
        font_family="gothra"
    ),
    h3_text_style=ft.TextStyle(
        color=ft.Colors.GREY_100,
        size=20,
        weight="bold",
        font_family="gothra"
    ),
    h4_text_style=ft.TextStyle(
        color=ft.Colors.GREY_200,
        size=18,
        weight="w500",
        font_family="gothra"
    ),
    h5_text_style=ft.TextStyle(
        color=ft.Colors.GREY_200,
        size=16,
        weight="w500",
        font_family="gothra"
    ),
    h6_text_style=ft.TextStyle(
        color=ft.Colors.GREY_200,
        size=14,
        font_family="gothra"
    ),
    
    # Ссылки - яркие
    a_text_style=ft.TextStyle(
        color=ft.Colors.CYAN_400,
        size=14,
        font_family="gothra"
    ),
    
    # Код в строке (inline)
    code_text_style=ft.TextStyle(
        color=ft.Colors.AMBER_200,
        size=6,
        font_family="gothra",
        bgcolor=ft.Colors.GREY_900  # Тёмный фон для кода
    ),
    
    # Блок кода
    codeblock_padding=ft.padding.all(12),
    codeblock_decoration=ft.BoxDecoration(
        bgcolor=ft.Colors.RED_ACCENT,
        border_radius=6
    ),
    
    # Жирный текст
    strong_text_style=ft.TextStyle(
        color=ft.Colors.GREEN,
        weight="bold",
        font_family="gothra"
    ),
    
    # Курсив
    em_text_style=ft.TextStyle(
        color=ft.Colors.DEEP_ORANGE_100,
        italic=True,
        font_family="gothra"
    ),
    
    # Зачёркнутый текст
    del_text_style=ft.TextStyle(
        color=ft.Colors.GREY_500,
        decoration="line_through",
        font_family="gothra"
    ),
    
    # Кавычки
    blockquote_text_style=ft.TextStyle(
        color=ft.Colors.GREY_300,
        size=14,
        italic=True,
        font_family="gothra"
    ),
    blockquote_padding=ft.padding.only(left=12, top=8, bottom=8, right=8),
    blockquote_decoration=ft.BoxDecoration(
        border=ft.border.only(
            left=ft.BorderSide(2, ft.Colors.CYAN_400)
        ),
        bgcolor=ft.Colors.BLUE_GREY
    ),
    
    # Пули списков
    list_bullet_text_style=ft.TextStyle(
        color=ft.Colors.CYAN_400,
        font_family="gothra"
    ),
    
    # Промежутки
    block_spacing=16,
    list_indent=24
)


md_style = make_md_style(
    "sofia",
    14,
    "#082B1E",
    "#042713",
    "#05166E",
    "#FFFFFF",
    "#0E3124",
    "#043926",
    "#97AC0B",
    "#C6641E",
    "#931CB7",
    "#043322",
    "#606CE9",
    "#004E31",
    "#065739",
    "#BC6069",
    "#10BACD",
    "#054B31",
    "#ED00BD",
    "manrope",
    "arsenal"
)

class Avatar(ft.Column):

    def __init__(
            self,
            role: str,
            image_path: str | Path,
            role_txt_color: str = "#BD5AA9",
            size: int = 50,
            font: str = "Roboto",
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
            weight=ft.FontWeight.BOLD,
            font_family=font,
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
            code_theme=ft.MarkdownCodeTheme.BROWN_PAPER,
            md_style_sheet=md_style,
            
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
        self.scroll = ft.ScrollMode.ALWAYS
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
        self.bgcolor = ft.Colors.with_opacity(0.5, ft.Colors.ON_SECONDARY_CONTAINER)

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
    src_dir = Path(__file__).parent.parent.parent.parent
    asts_dir = src_dir / "assets"
    fonts_dir = asts_dir / "fonts"
    gr = fonts_dir / "gothra.ttf"
    sf = fonts_dir / "sofia.ttf"
    ar = fonts_dir / "arsenal.ttf"
    mr = fonts_dir / "manrope.ttf"
    dsp = asts_dir / "prompts" / "default_system_prompt.md"
    dsp0 = dsp.read_text("utf-8")
    def main(page: ft.Page):
        page.window.icon = "icon.ico"
        page.fonts = {
            "gothra": str(gr),
            "sofia": str(sf),
            "arsenal": str(ar),
            "manrope": str(mr),
        }
        page.theme_mode = ft.ThemeMode.DARK
        cnt = MsgContainer(
            width=500,
            height=200,
            avatar_size=50,
            msg_txt=dsp0
        )
        page.add(cnt)
        

    ft.app(target=main, assets_dir="D:\\myworks\\agents\\warp_beast\\src\\assets")