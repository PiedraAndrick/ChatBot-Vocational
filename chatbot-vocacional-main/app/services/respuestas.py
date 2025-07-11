from app.db.pg import ConexionPostgres
from app.utils.httpResponses import create_error_message
from fastapi.responses import JSONResponse

class RespuestasService:
        #CONTRUCTOR
    def __init__(self):
        self.db_connection  = ConexionPostgres()

    def _get_db_connection(self):
        conn, error = self.db_connection.connect()
        if error:
            print(f"Error al conectar a PostgreSQL: {str(error)}")
            return None, JSONResponse(status_code=400, content=create_error_message("Ocurrio un error inesperado intentelo mas tarde"))
        return conn, None
    
    def create_respuesta(self,preg_id:int,resp_text:str,resp_tipo:str,resp_conten:str):
        conn, response = self._get_db_connection()
        if response:
            return response
        
        with conn.cursor() as cursor:
            # Verificar si se encuentra dentro de un test
            cursor.execute("""
                INSERT INTO respuestas (PREG_ID, RESP_TEXT, resp_tipo, resp_conten)
                VALUES (%s, %s, %s, %s)
                RETURNING RESP_ID
            """,(preg_id,resp_text , resp_tipo, resp_conten))
        conn.commit()
        conn.close()
        return
    
    def read_respuesta(self,resp_id:int):
        conn, response = self._get_db_connection()
        if response:
            return response
        
        with conn.cursor() as cursor:
            # Verificar si se encuentra dentro de un test
            cursor.execute("""
                SELECT * FROM respuestas WHERE RESP_ID = %s;
            """,(resp_id,))
            respuesta = cursor.fetchall()
        conn.close()
        return respuesta
    
    def update_respuesta(self,preg_id:int,resp_text:str,resp_tipo:str,resp_conten:str,resp_id:int):
        conn, response = self._get_db_connection()
        if response:
            return response
        
        with conn.cursor() as cursor:
            # Verificar si se encuentra dentro de un test
            cursor.execute("""
                UPDATE respuestas
                SET PREG_ID = %s, RESP_TEXT = %s, resp_tipo = %s, resp_conten = %s
                WHERE RESP_ID = %s
                RETURNING *
            """,(preg_id, resp_text, resp_tipo, resp_conten, resp_id))
        conn.commit()
        conn.close()
        return
    
    def delete_respuesta(self,resp_id:int):
        conn, response = self._get_db_connection()
        if response:
            return response
        
        with conn.cursor() as cursor:
            # Verificar si se encuentra dentro de un test
            cursor.execute("""
                DELETE FROM respuestas WHERE RESP_ID = %s RETURNING *
            """,(resp_id,))
        conn.commit()
        conn.close()
        return
