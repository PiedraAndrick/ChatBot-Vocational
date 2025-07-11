from fastapi import APIRouter,Depends
from app.models.preguntas import Pregunta
from app.controllers.preguntas import PreguntasController
from app.middlewares.auth import get_current_user
pregunta = APIRouter()
preguntaCtr = PreguntasController()

@pregunta.post("/preguntas/", response_model=dict)
def create_pregunta(pregunta: Pregunta,current_user: dict = Depends(get_current_user)):
    return preguntaCtr.create_pregunta(pregunta)

@pregunta.get("/preguntas/{preg_id}", response_model=dict)
def read_pregunta(preg_id: int,current_user: dict = Depends(get_current_user)):
    return preguntaCtr.read_pregunta(preg_id)

@pregunta.put("/preguntas/{preg_id}", response_model=dict)
def update_pregunta(preg_id: int, pregunta: Pregunta,current_user: dict = Depends(get_current_user)):
    return preguntaCtr.update_pregunta(preg_id,pregunta)

@pregunta.delete("/preguntas/{preg_id}", response_model=dict)
def delete_pregunta(preg_id: int,current_user: dict = Depends(get_current_user)):
    return preguntaCtr.delete_pregunta(preg_id)