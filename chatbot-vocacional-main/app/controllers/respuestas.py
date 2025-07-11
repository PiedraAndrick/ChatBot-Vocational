from fastapi.responses import JSONResponse
from app.services.respuestas import RespuestasService


class RespuestasController:
    #CONTRUCTOR
    def __init__(self):
        self.respSrv = RespuestasService()
        
    
    def create_respuesta(self,respuesta):
        resRespuesta = self.respSrv.create_respuesta(respuesta.preg_id,respuesta.resp_text,respuesta.resp_tipo,respuesta.resp_conten)
        if resRespuesta is not None : return resRespuesta
        return {
            "status": "OK",
            "data": [{
                "message": "Respuesta creada correctamente.",
                "tipo":"MENSAJE",
                "contenido": None
            }]
        }
    def read_respuesta(self,resp_id:int):
        respuesta = self.respSrv.read_respuesta(resp_id)
        if isinstance(respuesta,JSONResponse) : return respuesta
        return {
            "status": "OK",
            "data": [{
                "message": "Respuesta consultada correctamente.",
                "tipo":"MENSAJE",
                "contenido": respuesta
            }]
        }
        
    def update_respuesta(self,resp_id,respuesta):
        resRespuesta = self.respSrv.update_respuesta(respuesta.preg_id,respuesta.resp_text,respuesta.resp_tipo,respuesta.resp_conten,resp_id)
        if isinstance(resRespuesta,JSONResponse) : return resRespuesta
        return {
            "status": "OK",
            "data": [{
                "message": "Pregunta actualizada correctamente.",
                "tipo":"MENSAJE",
                "contenido": None
            }]
        }
    def delete_respuesta(self,resp_id):
        respuesta = self.respSrv.delete_respuesta(resp_id)
        if isinstance(respuesta,JSONResponse) : return respuesta
        return {
            "status": "OK",
            "data": [{
                "message": "Respuesta eliminda correctamente.",
                "tipo":"MENSAJE",
                "contenido": None
            }]
        }