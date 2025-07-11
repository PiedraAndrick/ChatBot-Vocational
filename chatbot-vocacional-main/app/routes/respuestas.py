from fastapi import APIRouter,Depends
from app.models.respuestas import Respuesta
from app.controllers.respuestas import RespuestasController
from app.middlewares.auth import get_current_user

respuesta = APIRouter()
respuestaCtr =  RespuestasController()

@respuesta.post("/respuestas/", response_model=dict)
def create_respuesta(respuesta: Respuesta,current_user: dict = Depends(get_current_user)):
    return respuestaCtr.create_respuesta(respuesta)

@respuesta.get("/respuestas/{resp_id}", response_model=dict)
def read_respuesta(resp_id: int,current_user: dict = Depends(get_current_user)):
    return respuestaCtr.read_respuesta(resp_id)

@respuesta.put("/respuestas/{resp_id}", response_model=dict)
def update_respuesta(resp_id: int, respuesta: Respuesta,current_user: dict = Depends(get_current_user)):
    return respuestaCtr.update_respuesta(resp_id,respuesta)

@respuesta.delete("/respuestas/{resp_id}", response_model=dict)
def delete_respuesta(resp_id: int,current_user: dict = Depends(get_current_user)):
    return respuestaCtr.delete_respuesta(resp_id)
