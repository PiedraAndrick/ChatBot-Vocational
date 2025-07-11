from pydantic import BaseModel
from typing import Optional

class Pregunta(BaseModel):
    flujo_id: Optional[int] = None
    preg_text: str
    preg_test: Optional[bool] = False
    test_id: Optional[int] = None