import os
from typing import Annotated
from fastapi import APIRouter, Cookie, Response
from fastapi.responses import FileResponse, JSONResponse
from app.models.Mensaje import Message
from app.controllers.chat import ChatController
from app.controllers.conversations import ConversationController
import uuid

chat = APIRouter()
chatController = ChatController()
conversationController = ConversationController()

@chat.get("/start")
async def start(response:Response):
    res = chatController.start_chat()
    if isinstance(res, JSONResponse):
        return res
    
    generated_uuid = uuid.uuid4()
    response.set_cookie(key="userSession", value=generated_uuid,httponly=True, samesite='none', secure=True) 
    return res

@chat.post("/chat")
async def ctrChat(
    prompt: Message,
    userSession:Annotated[str | None,Cookie()] = None
    ):
    conversationController.save_conversation(userSession,prompt.text,'USUARIO')
    res = chatController.chat_flujo(prompt,userSession)
    conversationController.save_conversation(userSession,res["data"],'BOT')
    return res



@chat.get("/download/{filename}")
async def mallaPdf(filename: str):

    file_location = f"app/public/pdf/mallas/{filename}"
    if os.path.exists(file_location):
        return FileResponse(file_location, media_type="application/pdf")
    else:
        return {
        "status": "Error",
        "data": [],
        "error": {
            "message": "Documento no encontrado"
        }
    }
   
