from app.db.pg import ConexionPostgres
from app.utils.httpResponses import create_error_message
from fastapi.responses import JSONResponse

class PreguntasService:
        #CONTRUCTOR
    def __init__(self):
        self.db_connection  = ConexionPostgres()

    def _get_db_connection(self):
        conn, error = self.db_connection.connect()
        if error:
            print(f"Error al conectar a PostgreSQL: {str(error)}")
            return None, JSONResponse(status_code=400, content=create_error_message("Ocurrio un error inesperado intentelo mas tarde"))
        return conn, None
    
    def create_pregunta(self,flujo_id:int,preg_text:str,preg_test:bool,test_id:int):
        conn, response = self._get_db_connection()
        if response:
            return response
        
        with conn.cursor() as cursor:
            # Verificar si se encuentra dentro de un test
            cursor.execute("""
                INSERT INTO preguntas (FLUJO_ID, PREG_TEXT, preg_test, TEST_ID)
                VALUES (%s, %s, %s, %s)
                RETURNING PREG_ID
            """,(flujo_id,preg_text , preg_test, test_id))
        conn.commit()
        conn.close()
        return
    
    def read_pregunta(self,preg_id:int):
        conn, response = self._get_db_connection()
        if response:
            return response
        
        with conn.cursor() as cursor:
            # Verificar si se encuentra dentro de un test
            cursor.execute("""
                SELECT * FROM preguntas WHERE PREG_ID = %s;
            """,(preg_id,))
            pregunta = cursor.fetchall()
        conn.close()
        return pregunta
    
    def update_pregunta(self,flujo_id:int,preg_text:str,preg_test:bool,test_id:int,preg_id:int):
        conn, response = self._get_db_connection()
        if response:
            return response
        
        with conn.cursor() as cursor:
            # Verificar si se encuentra dentro de un test
            cursor.execute("""
                UPDATE preguntas
                SET FLUJO_ID = %s, PREG_TEXT = %s, preg_test = %s, TEST_ID = %s
                WHERE PREG_ID = %s
                RETURNING *
            """,(flujo_id, preg_text, preg_test, test_id, preg_id))
        conn.commit()
        conn.close()
        return
    
    def delete_pregunta(self,preg_id:int):
        conn, response = self._get_db_connection()
        if response:
            return response
        
        with conn.cursor() as cursor:
            # Verificar si se encuentra dentro de un test
            cursor.execute("""
                DELETE FROM preguntas WHERE PREG_ID = %s RETURNING *
            """,(preg_id,))
        conn.commit()
        conn.close()
        return
