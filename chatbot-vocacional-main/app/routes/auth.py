from fastapi import APIRouter
from app.models.auth import UserLogin
from app.controllers.auth import AuthController

auth = APIRouter()
authCtr = AuthController()

@auth.post("/login/", response_model=dict)
def create_pregunta(usuario: UserLogin):
    return authCtr.login(usuario)
