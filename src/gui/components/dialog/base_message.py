# src/gui/components/dialog/base_message.py
import flet as ft
from pathlib import Path
from typing import Optional
from flet.core.types import ColorValue, OptionalNumber
from pydantic import BaseModel, Field

ASSETS_DIR = Path(__file__).parent.parent.parent.parent / "assets"


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

class AvatarTheme(BaseModel):
    size: int = Field(50, description="Размер аватара (px)")
    role_txt_color: ColorValue = Field("#3C0F33", description="Цвет текста роли")
    role_txt_size: int = Field(15, description="Размер шрифта подписи")
    font: str = Field("gothra", description="Шрифт подписи под аватаром")
    img_dict: dict = Field({"agent": "seal", "user": "tiger"}, description="Картинки по ролям")

class MsgTextTheme(BaseModel):
    md_theme: "MdTheme" = Field(default_factory=lambda: MdTheme())
    code_theme: ft.MarkdownCodeTheme = Field(
        default_factory=random_codetheme, description="Тема подсветки кода"
    )
    show_thoughts_button_text: str = Field("Мысли агента", description="Текст кнопки показа мыслей")
    thoughts_icon: str = Field(ft.Icons.DATA_OBJECT, description="Иконка для кнопки мыслей")

class MsgContainerTheme(BaseModel):
    width: OptionalNumber = Field(500, description="Ширина контейнера сообщения")
    height: OptionalNumber = Field(200, description="Высота контейнера сообщения")
    border_radius: int = Field(20, description="Радиус скругления")
    border_color: ColorValue = Field(ft.Colors.BLACK45, description="Цвет границы")
    border_width: float = Field(1.0, description="Толщина границы")
    bgcolor_opacity: float = Field(0.5, description="Прозрачность фона")
    bgcolor: ColorValue = Field(
        ft.Colors.ON_SECONDARY_CONTAINER, description="Базовый цвет фона"
    )
    avatar_theme: AvatarTheme = Field(default=AvatarTheme())
    msg_txt_theme: MsgTextTheme = Field(default=MsgTextTheme())

class ChatContainerTheme(BaseModel):
    width: OptionalNumber = Field(550, description="Ширина чата")
    height: OptionalNumber = Field(670, description="Высота чата")
    bgcolor: ColorValue = Field(ft.Colors.ON_SURFACE, description="Фон чата")
    scroll: ft.ScrollMode = Field(ft.ScrollMode.ALWAYS, description="Режим скролла")
    block_spacing: int = Field(15, description="Отступ между сообщениями")
    border_radius: int = Field(25)



class Avatar(ft.Column):

    def __init__(
            self,
            role: str,
            theme: AvatarTheme = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if theme is None:
            theme = AvatarTheme()
        self.role = role
        self.img_path = ASSETS_DIR / f"{theme.img_dict[role]}.png"
        #надо будет к page.data["assets_path"]
        self.role_txt_color = theme.role_txt_color
        self.size = theme.size
        self.width = self.size+15

        

        self.pic = ft.Image(
            src=str(self.img_path),
            width=self.size,
            height=self.size
        )
        self.role_txt = ft.Text(
            value=self.role.upper(),
            #text_align=ft.TextAlign.CENTER,
            color=self.role_txt_color,
            weight=ft.FontWeight.BOLD,
            font_family=theme.font,
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
            theme: Optional[MsgTextTheme] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.msg_txt = msg_txt
        self.thought_txt = thought_txt
        if theme is None:
            theme = MsgTextTheme()



        self.msg_txt_mkdn = ft.Markdown(
            value=self.msg_txt,
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_FLAVORED,
            code_theme=theme.code_theme,
            md_style_sheet=create_markdown_style(theme.md_theme)
            
        )
        te = True if self.thought_txt is not None else False
        self.thought_txt_mkdn = ft.Markdown(
            value=self.thought_txt,
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_FLAVORED,
            code_theme=theme.code_theme,
            md_style_sheet=create_markdown_style(theme.md_theme),
            visible=False,
        )
        self.thought_txt_btn = ft.TextButton(
            text=theme.show_thoughts_button_text,
            icon=theme.thoughts_icon,
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
            role: str,
            msg_txt: str,
            thought_txt: Optional[str] = None,
            theme: Optional[MsgContainerTheme] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if theme is None:
            theme = MsgContainerTheme()
        self.width = theme.width
        self.height = theme.height
        self.border_radius = ft.border_radius.all(theme.border_radius)
        self.border = ft.border.all(theme.border_width, theme.border_color)

        
        self.avatar = Avatar(role, theme.avatar_theme)
        self.txtmsgcolumn = MsgTextColumn(
            msg_txt=msg_txt,
            thought_txt=thought_txt,
            theme=theme.msg_txt_theme
        )

        self.content = ft.Row(
            controls=[
                self.avatar,
                self.txtmsgcolumn
            ],

        )
        self.bgcolor = ft.Colors.with_opacity(theme.bgcolor_opacity, theme.bgcolor)


class ChatContainer(ft.Container):

    def __init__(
            self,
            theme: Optional[ChatContainerTheme] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if theme is None:
            theme = ChatContainerTheme()
        self.width = theme.width
        self.height = theme.height


        self.bgcolor = theme.bgcolor
        self.border_radius = ft.border_radius.all(theme.border_radius)

        self.chat_column = ft.Column(
            expand=True,
            scroll=theme.scroll,
            spacing=theme.block_spacing,
        )
        self.content = self.chat_column

    def add_msg_container(self, mc: MsgContainer):
        self.chat_column.controls.append(mc)
        self.update()

        



if __name__ == '__main__':
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

        def pr(t:str):
            print(t)

        page.data = {
            "pr": pr,
        }
        

        cct = ChatContainer(theme=ChatContainerTheme(bgcolor="#4FC4C4"))
        m0 = MsgContainer("user", "kjljlkj;o;j;sdfskfj;doifdgijbfgj")
        page.add(cct)
        cct.add_msg_container(m0)
        for _ in range(6):
            m = MsgContainer("agent", "iouhihuou", "iluuy")
            cct.add_msg_container(m)
        


    ft.app(target=main, assets_dir="D:\\myworks\\agents\\warp_beast\\src\\assets")