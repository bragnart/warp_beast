# src/gui/components/dialog/base_message.py
import flet as ft
from pathlib import Path
from typing import Optional
from flet.core.types import ColorValue, OptionalNumber
from pydantic import BaseModel, Field

# -----------------------------------------------------------------------------
# 1. Конфигурация темы (Pydantic V2)
# -----------------------------------------------------------------------------
class MdTheme(BaseModel):
    """
    Класс конфигурации для стилей Markdown.
    Позволяет задать все цвета и шрифты в одном месте с валидацией.
    """
    # Шрифты
    font_main: str = Field("sofia", description="Шрифт для основного текста")
    font_code: str = Field("manrope", description="Шрифт для блоков кода (моноширинный)")
    font_quote: str = Field("arsenal", description="Шрифт для цитат")
    
    # Размеры
    text_size: int = Field(14, description="Базовая размерность текста (px)")
    header_scale: float = Field(1.15, description="Множитель увеличения заголовков (h6 -> h1)")

    # Цвета текста
    color_main: ColorValue = Field("#082B1E", description="Цвет основного текста")
    color_headers: ColorValue = Field("#042713", description="Цвет заголовков (h1-h6)")
    color_link: ColorValue = Field("#05166E", description="Цвет ссылок")
    color_strong: ColorValue = Field("#0E3124", description="Цвет жирного текста")
    color_em: ColorValue = Field("#043926", description="Цвет курсива")
    color_del: ColorValue = Field("#465000", description="Цвет зачеркнутого текста")
    
    # Цвета элементов списка и таблиц
    color_list_bullet: ColorValue = Field("#606CE9", description="Цвет маркеров списка")
    color_table_head: ColorValue = Field("#004E31", description="Цвет текста заголовков таблицы")
    color_table_body: ColorValue = Field("#065739", description="Цвет текста ячеек таблицы")
    
    # Цвета блоков (фоны и границы)
    color_code_text: ColorValue = Field("#5D0DA8", description="Цвет текста внутри inline кода")
    color_code_bg: ColorValue = Field("#7E10DE", description="Основной цвет оформления блока кода (используется для фона с прозрачностью)")
    color_quote_text: ColorValue = Field("#931CB7", description="Цвет текста цитаты")
    color_quote_border: ColorValue = Field("#ED00BD", description="Цвет боковой линии цитаты")
    color_quote_bg: ColorValue = Field("#10BACD", description="Фон цитаты")
    
    color_checkbox: ColorValue = Field("#043322", description="Цвет текста чекбоксов")
    color_img_text: ColorValue = Field("#FFFFFF", description="Цвет alt-текста картинок")
    color_divider: ColorValue = Field("#054B31", description="Цвет разделительной линии (hr)")


# -----------------------------------------------------------------------------
# 2. Фабрика стилей
# -----------------------------------------------------------------------------
def create_markdown_style(theme: MdTheme) -> ft.MarkdownStyleSheet:
    """
    Генерирует ft.MarkdownStyleSheet на основе переданной Pydantic-темы.
    """
    
    # Общие параметры, которые есть ВЕЗДЕ (шрифт и размер)
    # Цвет мы сюда НЕ кладем, чтобы не было конфликтов
    common_props = {
        "font_family": theme.font_main,
        "size": theme.text_size,
    }
    
    # 1. Генерация стилей заголовков
    heading_styles = {}
    current_size = theme.text_size
    
    for i in range(6, 0, -1):
        heading_styles[f"h{i}_text_style"] = ft.TextStyle(
            font_family=theme.font_main,
            color=theme.color_headers,
            size=int(current_size),
            weight=ft.FontWeight.BOLD,
        )
        current_size *= theme.header_scale

    # 2. Сборка объекта
    return ft.MarkdownStyleSheet(
        # --- Основной текст ---
        # Тут добавляем color_main к общим свойствам
        p_text_style=ft.TextStyle(**common_props, color=theme.color_main),
        
        # --- Ссылки (переопределяем цвет) ---
        a_text_style=ft.TextStyle(**common_props, color=theme.color_link),
        
        # --- Жирный / Курсив / Зачеркнутый ---
        strong_text_style=ft.TextStyle(**common_props, color=theme.color_strong, weight=ft.FontWeight.BOLD),
        em_text_style=ft.TextStyle(**common_props, color=theme.color_em, italic=True),
        del_text_style=ft.TextStyle(**common_props, color=theme.color_del, decoration=ft.TextDecoration.LINE_THROUGH),
        
        # --- Списки ---
        list_bullet_text_style=ft.TextStyle(**common_props, color=theme.color_list_bullet, decoration=ft.TextDecoration.UNDERLINE, decoration_style=ft.TextDecorationStyle.DOTTED),
        checkbox_text_style=ft.TextStyle(**common_props, color=theme.color_checkbox),
        
        # --- Заголовки ---
        **heading_styles,

        # --- Код ---
        code_text_style=ft.TextStyle(
            font_family=theme.font_code,
            size=theme.text_size,
            color=theme.color_code_text,
            bgcolor=ft.Colors.with_opacity(0.1, theme.color_code_bg) if theme.color_code_bg else None
        ),
        codeblock_decoration=ft.BoxDecoration(
            #bgcolor=ft.Colors.with_opacity(0.05, theme.color_code_bg),
            border=ft.border.all(2, ft.Colors.CYAN_300),
            border_radius=ft.border_radius.only(bottom_left=20, top_right=20, bottom_right=13, top_left=13)
        ),

        # --- Цитаты ---
        blockquote_text_style=ft.TextStyle(
            font_family=theme.font_quote,
            size=theme.text_size,
            color=theme.color_quote_text,
            italic=True
        ),
        blockquote_decoration=ft.BoxDecoration(
            bgcolor=ft.Colors.with_opacity(0.1, theme.color_quote_bg),
            border=ft.border.only(left=ft.BorderSide(4, theme.color_quote_border)),
            border_radius=ft.border_radius.only(top_right=10, bottom_right=10)
        ),

        # --- Таблицы ---
        table_head_text_style=ft.TextStyle(**common_props, color=theme.color_table_head, weight=ft.FontWeight.BOLD),
        table_body_text_style=ft.TextStyle(**common_props, color=theme.color_table_body),
        table_cells_decoration=ft.BoxDecoration(
             border=ft.border.all(0.5, ft.Colors.with_opacity(0.2, theme.color_table_body))
        ),

        # --- Разное ---
        img_text_style=ft.TextStyle(**common_props, color=theme.color_img_text, italic=True),
        horizontal_rule_decoration=ft.BoxDecoration(
            border=ft.border.all(1, theme.color_divider)
        ),
        
        block_spacing=15,
    )


# -----------------------------------------------------------------------------
# 3. Пример использования
# -----------------------------------------------------------------------------

# Создаем конфиг темы (валидация происходит здесь)
my_theme_config = MdTheme()
# Генерируем стиль
final_style = create_markdown_style(my_theme_config)

# Используем в Flet
# ft.Markdown(
#    value="# Привет \nТекст...", 
#    md_style_sheet=final_style,
#    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB  # ВАЖНО для таблиц и зачеркивания!
# )


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
            #bgcolor=cd_block_color,
            border=ft.border.all(1, ft.Colors.BLUE_ACCENT),
            border_radius=ft.border_radius.all(13),
            shadow=ft.BoxShadow(color=ft.Colors.BLUE_GREY_300, blur_style=ft.ShadowBlurStyle.NORMAL)
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
            bgcolor=line_color,
        )
    )
    return mds


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
#DRAGULA, ATOM, хопскотч, грувбокс дарк, монокай, шейдс оф
DF_CODETHEMES = [
    ft.MarkdownCodeTheme.AGATE,
    ft.MarkdownCodeTheme.DRAGULA,
    ft.MarkdownCodeTheme.ATOM_ONE_DARK_REASONABLE,
    ft.MarkdownCodeTheme.HOPSCOTCH,
    ft.MarkdownCodeTheme.GRUVBOX_DARK,
    ft.MarkdownCodeTheme.MONOKAI,
    ft.MarkdownCodeTheme.MONOKAI_SUBLIME,
    ft.MarkdownCodeTheme.SHADES_OF_PURPLE,
]

def random_codetheme():
    from random import choice
    return choice(DF_CODETHEMES)


class Avatar(ft.Column):

    def __init__(
            self,
            role: str,
            image_path: str | Path,
            role_txt_color: str = "#3C0F33",
            size: int = 50,
            font: str = "gothra",
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
            txt_md_style: Optional[ft.MarkdownStyleSheet] = None,
            tht_md_style: Optional[ft.MarkdownStyleSheet] = None,
            codetheme: Optional[ft.MarkdownCodeTheme] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.msg_txt = msg_txt
        self.thought_txt = thought_txt
        self.txt_md_style = txt_md_style or final_style
        self.tht_md_style = tht_md_style or final_style
        self.codetheme = codetheme if codetheme is not None else random_codetheme()



        self.msg_txt_mkdn = ft.Markdown(
            value=self.msg_txt,
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_FLAVORED,
            code_theme=self.codetheme,
            md_style_sheet=self.txt_md_style,
            
        )
        te = True if self.thought_txt is not None else False
        self.thought_txt_mkdn = ft.Markdown(
            value=self.thought_txt,
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_FLAVORED,
            code_theme=self.codetheme,
            md_style_sheet=self.tht_md_style,
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
            img: str = "seal",
            **kwargs
    ):
        super().__init__(**kwargs)
        self.width = width
        self.height = height
        self.border_radius = ft.border_radius.only(top_left=20, bottom_left=20)
        self.border = ft.border.all(1, ft.Colors.BLACK45)

        av_img = Path(f"src/assets/{img}.png")
        
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
    dsp0 = """```python
    class MsgTextColumn(ft.Column):

    def __init__(
            self,
            msg_txt: str,
            thought_txt: Optional[str] = None,
            txt_md_style: Optional[ft.MarkdownStyleSheet] = None,
            tht_md_style: Optional[ft.MarkdownStyleSheet] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.msg_txt = msg_txt
        self.thought_txt = thought_txt
        self.txt_md_style = txt_md_style or md_style
        self.tht_md_style = tht_md_style or md_style
```

#### Проверка

Ну сперва проверим **жирный текст**, *курсив*, ~~зачеркнутый~~ или __вот__
Потом ``import inline code`` и также
>простая такая цитата

###### Тест

##### Test

#### Test

### Test

## Test

# Test

___________________________________

"""
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
            msg_txt=dsp0,
            thought_txt=dsp0,
        )
        page.add(cnt)
        

    ft.app(target=main, assets_dir="D:\\myworks\\agents\\warp_beast\\src\\assets")