from pydantic import BaseModel,Field

class Message(BaseModel):
    text: list[str] = Field(min_items=1, max_items=10, default=[])
