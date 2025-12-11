# src/gui/components/dialog/msg_sender.py
import flet as ft
from typing import Optional
from pathlib import Path
from pydantic import BaseModel, Field

class MsgSenderTheme(BaseModel):
    width: int = Field(550)
    height: int = Field(90)
    input_font: str = Field("arsenal")
    input_txtsize: int = Field(16)
    input_bgcolor: str = Field("#A9AEE6")
    input_color: str = Field("#74046B")
    input_bordercolor: str = Field("#4366E6")
    input_borderradius: int = Field(15)
    btn_icon: str = Field("send")
    attach_icon: str = Field("attach_file")  # Новое поле

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
        self.attached_image_path: Optional[Path] = None
        
        # FilePicker для выбора изображений
        self.file_picker = ft.FilePicker(
            on_result=self._on_file_picked
        )
        
        self._preview = ft.Image(
            src=None,
            width=50,
            height=50
        )
        # Превью прикреплённого изображения
        self.image_preview = ft.Container(
            content=ft.Row([
                self._preview,
                ft.IconButton(
                    icon=ft.Icons.CLOSE,
                    icon_size=16,
                    on_click=self._remove_image
                )
            ]),
            visible=False,
            bgcolor=ft.Colors.with_opacity(0.2, "#F69E9E"),
            border_radius=10,
            padding=5,
            bottom=0,
            right=0,
        )
        
        self.input = ft.TextField(
            multiline=True,
            min_lines=3,
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
        
        # Кнопка прикрепления
        self.attach_btn = ft.IconButton(
            icon=theme.attach_icon,
            right=0,
            bottom=0,
            on_click=lambda _: self.file_picker.pick_files(
                allowed_extensions=["png", "jpg", "jpeg", "gif", "webp"],
                dialog_title="Выбери изображение"
            ),
            opacity=0.5,
        )
        
        # Кнопка отправки
        self.send_btn = ft.IconButton(
            icon=theme.btn_icon,
            right=0,
            top=0,
            on_click=self._send,
            opacity=0.5,
        )
        
        self.controls.append(self.file_picker)
        self.controls.append(self.input)
        self.controls.append(self.image_preview)
        self.controls.append(self.attach_btn)
        self.controls.append(self.send_btn)
    
    def _on_file_picked(self, e: ft.FilePickerResultEvent):
        """Обработчик выбора файла"""
        if e.files and len(e.files) > 0:
            file = e.files[0]
            self.attached_image_path = Path(file.path)
            
            # Показываем превью
            self._preview.src = str(self.attached_image_path)
            self.image_preview.visible = True
            self.attach_btn.visible = False
            self.update()
    
    def _remove_image(self, e):
        """Удаление прикреплённого изображения"""
        self.attached_image_path = None
        self.image_preview.visible = False
        self.attach_btn.visible = True
        self.update()
    
    async def _send(self, e):
        msg_txt = self.input.value
        if msg_txt.strip() or self.attached_image_path:
            self.input.value = ""
            
            # Передаём и текст, и путь к изображению
            self.parent._send(
                msg_txt=msg_txt,
                image_path=self.attached_image_path
            )
            
            # Сбрасываем изображение после отправки
            self.attached_image_path = None
            self.image_preview.visible = False
            self.update()
