from app.db.pg import ConexionPostgres
from app.utils.httpResponses import create_error_message
from fastapi.responses import JSONResponse

class ConversationService:
        #CONTRUCTOR
    def __init__(self):
        self.db_connection  = ConexionPostgres()

    def _get_db_connection(self):
        conn, error = self.db_connection.connect()
        if error:
            print(f"Error al conectar a PostgreSQL: {str(error)}")
            return None, JSONResponse(status_code=400, content=create_error_message("Ocurrio un error inesperado intentelo mas tarde"))
        return conn, None
    
    def save_conversation(self,user_session:str,message:str,emitter:str, date:str):
        conn, response = self._get_db_connection()
        if response:
            return response
        
        with conn.cursor() as cursor:
            # Verificar si se encuentra dentro de un test
            cursor.execute("""
                INSERT INTO conversaciones (conv_cookie, conv_msj, conv_emis, conv_fecha) VALUES(%s,%s,%s,%s);
            """,(user_session,message,emitter,date))
        conn.commit()
        conn.close()
        return
    