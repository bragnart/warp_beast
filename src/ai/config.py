# src/ai/config.py
from __future__ import annotations
import yaml
from pathlib import Path
from pydantic import BaseModel, Field

APP_DIR = Path(__file__).parent.parent
DATA_DIR = APP_DIR / "assets"

bpf = DATA_DIR / "prompts" / "default_system_prompt.md"
DEFAULT_SYSTEM_PROMPT = bpf.read_text("utf-8")
DEFAULT_RUN_INSTRUCTION = "Поразмысли и ответь юзеру корректно."

class AIConfig(BaseModel):

    agent_id: str = Field(default="WarpBeast")
    user_id: str = Field(default="User")
    model_name: str = Field(default="google/gemini-2.5-flash-lite-preview-09-2025", description="Имя модели")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    reasoning: bool = Field(default=True)
    max_tokens: int = Field(default=8000)
    timeout: float = Field(default=30.0)
    system_prompt: str = Field(default=DEFAULT_SYSTEM_PROMPT)
    run_instruction: str = Field(default=DEFAULT_RUN_INSTRUCTION)
    enable_mem0: bool = Field(default=True)

    def to_dict(self) -> dict:
        return self.model_dump()
    
    @classmethod
    def from_dict(cls, data) -> "AIConfig":
        return cls.model_validate(data)
    
    def save_to_yaml(self, filepath: str | Path):
        if not isinstance(filepath, Path):
            filepath = Path(filepath)

        with open(filepath, "w", encoding="utf-8") as file:
            yaml.safe_dump(self.to_dict(), file, sort_keys=False, allow_unicode=True)

    @classmethod
    def load_from_yaml(cls, filepath: str | Path):
        if not isinstance(filepath, Path):
            filepath = Path(filepath)

        with open(filepath, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
        
        return cls.model_validate(data)