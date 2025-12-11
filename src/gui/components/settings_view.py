# src/gui/components/settings_view.py
import flet as ft
from typing import Optional, Callable
from pydantic import BaseModel, Field
from src.ai import AIConfig

class SettingsViewTheme(BaseModel):
    """Тема для окна настроек"""
    width: int = Field(550)
    height: int = Field(670)
    bgcolor: str = Field("#3D5A80")
    border_radius: int = Field(25)
    
    title_text: str = Field("⚙️ Настройка сессии")
    title_color: str = Field("#FFFFFF")
    title_size: int = Field(24)
    title_font: str = Field("gothra")
    
    label_color: str = Field("#E0FBFC")
    label_size: int = Field(16)
    label_font: str = Field("arsenal")
    
    input_bgcolor: str = Field("#98C1D9")
    input_color: str = Field("#293241")
    input_font: str = Field("sofia")
    
    btn_start_text: str = Field("🚀 Запустить сессию")
    btn_start_color: str = Field("#06FFA5")
    btn_start_text_color: str = Field("#000000")

class SettingsView(ft.View):
    def __init__(
        self,
        theme: Optional[SettingsViewTheme] = None,
        on_start_callback: Optional[Callable] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        

        if theme is None:
            theme = SettingsViewTheme()
        
        self.theme = theme
        
        self.route = "settings_view"
        self.bgcolor = theme.bgcolor
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.on_start_callback = on_start_callback
        self.expand = True
        # Создаём конфиг по умолчанию
        self.default_config = AIConfig()
        self.visible = True
        
        # Заголовок
        self.title = ft.Text(
            value=theme.title_text,
            size=theme.title_size,
            color=theme.title_color,
            font_family=theme.title_font,
            weight=ft.FontWeight.BOLD,
        )
        
        # Поля ввода
        self.agent_id_input = self._create_textfield(
            label="🤖 ID Агента",
            value=self.default_config.agent_id,
            hint="WarpBeast"
        )
        
        self.user_id_input = self._create_textfield(
            label="👤 ID Пользователя",
            value=self.default_config.user_id,
            hint="User"
        )
        
        self.model_input = self._create_textfield(
            label="🧠 Модель",
            value=self.default_config.model_name,
            hint="Модель"
        )

        # Слайдер температуры
        self.temp_value_text = ft.Text(
            value=f"{self.default_config.temperature:.2f}",
            size=16,
            color=theme.label_color,
        )
        
        self.temp_slider = ft.Slider(
            label="🌡️ Temperature: {value}",
            min=0.0,
            max=2.0,
            value=self.default_config.temperature,
            divisions=20,
            on_change=self._on_temp_change,
            active_color=ft.Colors.CYAN_400,
            thumb_color=ft.Colors.CYAN_700,
        )
        
        # Слайдер max_tokens
        self.tokens_value_text = ft.Text(
            value=f"{self.default_config.max_tokens}",
            size=16,
            color=theme.label_color,
        )
        
        self.tokens_slider = ft.Slider(
            label="🔢 Max Tokens: {value}",
            min=1000,
            max=32000,
            value=self.default_config.max_tokens,
            divisions=31,
            on_change=self._on_tokens_change,
            active_color=ft.Colors.PURPLE_400,
            thumb_color=ft.Colors.PURPLE_700,
        )
        
        # Переключатели
        self.reasoning_switch = ft.Switch(
            label="💭 Reasoning (думающие модели)",
            value=self.default_config.reasoning,
            active_color=ft.Colors.GREEN_400,
            label_style=ft.TextStyle(
                color=theme.label_color,
                font_family=theme.label_font,
            ),
        )
        
        self.mem0_switch = ft.Switch(
            label="🧠 Mem0 (долговременная память)",
            value=self.default_config.enable_mem0,
            active_color=ft.Colors.BLUE_400,
            label_style=ft.TextStyle(
                color=theme.label_color,
                font_family=theme.label_font,
            ),
        )
        
        # Кнопка запуска
        self.start_btn = ft.ElevatedButton(
            text=theme.btn_start_text,
            bgcolor=theme.btn_start_color,
            color=theme.btn_start_text_color,
            width=300,
            height=50,
            on_click=self._on_start_click,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=15),
            ),
        )
        
        # Контейнер с формой
        self.form_container = ft.Container(
            width=theme.width,
            height=theme.height,
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            border_radius=ft.border_radius.all(theme.border_radius),
            padding=30,
            content=ft.Column(
                controls=[
                    self.title,
                    ft.Divider(height=20, color="transparent"),
                    self.agent_id_input,
                    self.user_id_input,
                    self.model_input,
                    ft.Divider(height=10, color="transparent"),
                    ft.Row([
                        ft.Text(
                            "🌡️ Temperature:",
                            size=theme.label_size,
                            color=theme.label_color,
                            font_family=theme.label_font,
                        ),
                        self.temp_value_text,
                    ]),
                    self.temp_slider,
                    ft.Divider(height=10, color="transparent"),
                    ft.Row([
                        ft.Text(
                            "🔢 Max Tokens:",
                            size=theme.label_size,
                            color=theme.label_color,
                            font_family=theme.label_font,
                        ),
                        self.tokens_value_text,
                    ]),
                    self.tokens_slider,
                    ft.Divider(height=10, color="transparent"),
                    self.reasoning_switch,
                    self.mem0_switch,
                    ft.Divider(height=20, color="transparent"),
                    ft.Row([self.start_btn], alignment=ft.MainAxisAlignment.CENTER),
                ],
                scroll=ft.ScrollMode.AUTO,
                spacing=10,
            ),
        )
        
        self.controls = [self.form_container]
    
    def _create_textfield(self, label: str, value: str, hint: str) -> ft.TextField:
        """Создаёт стилизованное текстовое поле"""
        return ft.TextField(
            label=label,
            value=value,
            hint_text=hint,
            width=450,
            bgcolor=self.theme.input_bgcolor,
            color=self.theme.input_color,
            label_style=ft.TextStyle(
                color=self.theme.label_color,
                font_family=self.theme.label_font,
            ),
            text_style=ft.TextStyle(
                font_family=self.theme.input_font,
            ),
            border_radius=10,
        )
    
    def _on_temp_change(self, e):
        """Обработчик изменения температуры"""
        self.temp_value_text.value = f"{e.control.value:.2f}"
        self.temp_value_text.update()
    
    def _on_tokens_change(self, e):
        """Обработчик изменения max_tokens"""
        self.tokens_value_text.value = f"{int(e.control.value)}"
        self.tokens_value_text.update()
    
    def _on_start_click(self, e):
        """Обработчик нажатия на кнопку запуска"""
        # Собираем конфиг из полей
        config = AIConfig(
            agent_id=self.agent_id_input.value,
            user_id=self.user_id_input.value,
            model_name=self.model_input.value,
            temperature=self.temp_slider.value,
            max_tokens=int(self.tokens_slider.value),
            reasoning=self.reasoning_switch.value,
            enable_mem0=self.mem0_switch.value,
        )
        
        
        # Вызываем callback если есть
        if self.on_start_callback:
            self.on_start_callback(config)
        

