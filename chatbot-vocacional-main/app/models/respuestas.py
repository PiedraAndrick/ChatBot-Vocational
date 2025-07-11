from pydantic import BaseModel
from typing import Optional

class Respuesta(BaseModel):
    preg_id: Optional[int] = None
    resp_text: str
    resp_tipo: Optional[str] = None
    resp_conten: Optional[str] = None
