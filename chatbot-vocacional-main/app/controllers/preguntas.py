from fastapi.responses import JSONResponse
from app.services.preguntas import PreguntasService


class PreguntasController:
    #CONTRUCTOR
    def __init__(self):
        self.pregSrv = PreguntasService()
        
    
    def create_pregunta(self,pregunta):
        pregunta = self.pregSrv.create_pregunta(pregunta.flujo_id,pregunta.preg_text,pregunta.preg_test,pregunta.test_id)
        if pregunta is not None : return pregunta
        return {
            "status": "OK",
            "data": [{
                "message": "Pregunta creada correctamente.",
                "tipo":"MENSAJE",
                "contenido": None
            }]
        }
    def read_pregunta(self,preg_id:int):
        pregunta = self.pregSrv.read_pregunta(preg_id)
        if isinstance(pregunta,JSONResponse) : return pregunta
        return {
            "status": "OK",
            "data": [{
                "message": "Pregunta consultada correctamente.",
                "tipo":"MENSAJE",
                "contenido": pregunta
            }]
        }
        
    def update_pregunta(self,preg_id,pregunta):
        pregunta = self.pregSrv.update_pregunta(pregunta.flujo_id,pregunta.preg_text,pregunta.preg_test,pregunta.test_id,preg_id)
        if isinstance(pregunta,JSONResponse) : return pregunta
        return {
            "status": "OK",
            "data": [{
                "message": "Pregunta actualizada correctamente.",
                "tipo":"MENSAJE",
                "contenido": None
            }]
        }
    def delete_pregunta(self,preg_id):
        pregunta = self.pregSrv.delete_pregunta(preg_id)
        if isinstance(pregunta,JSONResponse) : return pregunta
        return {
            "status": "OK",
            "data": [{
                "message": "Pregunta eliminda correctamente.",
                "tipo":"MENSAJE",
                "contenido": None
            }]
        }