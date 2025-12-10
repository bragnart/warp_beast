# src/gui/constants.py
from pathlib import Path

ASSETS_PATH = Path(__file__).parent.parent / "assets"
FONT_PATH = ASSETS_PATH / "fonts"
FONT_DICT = {p.stem: str(p) for p in FONT_PATH.glob("*.ttf")}
