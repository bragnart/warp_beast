# src/ai/output_models.py
from pydantic import BaseModel, Field

class ResponseModel(BaseModel):

    def to_history(self):
        return str(self.model_dump(mode="json"))

class TandT(ResponseModel):
    """Стандартный ответ чат-агента."""
    text: str = Field(..., description="Текст ответа пользователю.")
    thought: str = Field(..., description="Скрытые мысли или рассуждения (Chain of Thought).")

    def to_history(self):
        t = f"{self.text}\n[Скрытые мысли: {self.thought}]"
        return t
