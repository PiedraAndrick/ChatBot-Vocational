from app.db.pg import ConexionPostgres
from app.utils.httpResponses import create_error_message
from fastapi.responses import JSONResponse

class AnswerService:
        #CONTRUCTOR
    def __init__(self):
        self.db_connection = ConexionPostgres()

    def _get_db_connection(self):
        conn, error = self.db_connection.connect()
        if error:
            print(f"Error al conectar a PostgreSQL: {str(error)}")
            return None, JSONResponse(status_code=400, content=create_error_message("Ocurrio un error inesperado intentelo mas tarde"))
        return conn, None
    
    def get_answers_by_quetion(self,question_id:int):
        conn, response = self._get_db_connection()
        if response:
            return response
        
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM respuestas where preg_id = %s;
            """,(question_id,))
            answers = cursor.fetchall()

        conn.close()
        return answers