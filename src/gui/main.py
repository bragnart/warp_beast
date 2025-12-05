import flet as ft
from .app_context import AppContext
from .components import ConfigControl, RequestControl





def main(page: ft.Page):
    page.window.width = 550
    page.window.height = 705
    page.window.frameless = True
    page.window.bgcolor = ft.Colors.TRANSPARENT
    page.window.icon = ft.Icons.BUG_REPORT
    page.bgcolor = ft.Colors.TRANSPARENT
    # page.opacity = 0.7
    
    app_context = AppContext()
    app_context._page = page

    config_control = ConfigControl(app_context=app_context)
    request_control = RequestControl(app_context=app_context)

    def _on_keyboard_event(e: ft.KeyboardEvent):
        if e.key == "Escape":
            page.window.close()
        if e.key == "Q" and e.ctrl:
            page.window.close()
        if e.key == "Enter" and e.ctrl:
            if len(request_control.request_input.value) > 1:
                request_control._on_send(e)

    page.on_keyboard_event = _on_keyboard_event

    page.add(config_control)
    page.add(request_control)



ft.app(target=main, assets_dir="src/assets")


