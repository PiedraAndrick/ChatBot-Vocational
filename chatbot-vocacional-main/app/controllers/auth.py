from app.services.auth import AuthService
from app.utils.passHandle import verify_pass
from app.utils.jwtHandle import create_access_token
class AuthController:
    #CONTRUCTOR
    def __init__(self):
        self.authSrv = AuthService()
        
    
    def login(self,usuario_data):
        #BUSCAR EL USUARIO
        usuario = self.authSrv.get_user_by_email(usuario_data.email)
        if len(usuario) == 0: return {
            "status": "ERROR",
            "data": [{
                "message": "Credenciales Incorrectas",
                "tipo":"MENSAJE",
                "contenido": None
            }]
        }
        #VALIDAR LA CONTRASEÑA
        pass_hash = usuario[0][3]
        is_correct = verify_pass(usuario_data.password, pass_hash)
        if not is_correct: return {
            "status": "ERROR",
            "data": [{
                "message": "Credenciales Incorrectas",
                "tipo":"MENSAJE",
                "contenido": None
            }]
        }
        #GENERAR EL TOKEN
        jwt = create_access_token({
            "user_id":usuario[0][0],
            "user_email":usuario[0][2],
        })
        
        return {
            "status": "OK",
            "data": [{
                "message": "Pregunta creada correctamente.",
                "tipo":"MENSAJE",
                "contenido": jwt
            }]
        }
