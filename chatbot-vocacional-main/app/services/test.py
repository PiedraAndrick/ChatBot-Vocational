from fastapi.responses import JSONResponse
from app.utils.httpResponses import create_error_message
from app.db.pg import ConexionPostgres

class TestService:
    
    #CONTRUCTOR
    def __init__(self):
        self.db_connection  = ConexionPostgres()
    
    def _get_db_connection(self):
        conn, error = self.db_connection.connect()
        if error:
            print(f"Error al conectar a PostgreSQL: {str(error)}")
            return None, JSONResponse(status_code=400, content=create_error_message("Ocurrio un error inesperado intentelo mas tarde"))
        return conn, None
    
    def check_test(self,user_session:str):
        conn, response = self._get_db_connection()
        if response:
            return response
        
        with conn.cursor() as cursor:
            # Verificar si se encuentra dentro de un test
            cursor.execute("""
                SELECT score_id, score_status, score_quest, test_id, score_content, score_name, score_email
                FROM scores
                WHERE score_cookie = %s AND score_status = %s;
            """, (user_session, "ACTIVO"))
            user_score = cursor.fetchall()
        
        conn.close()
        return user_score
    
    def start_test(self,user_session:str,test_id:int):
        conn, response = self._get_db_connection()
        if response:
            return response
        
        with conn.cursor() as cursor:
            # Insertar registro que inicia del test
            cursor.execute("""
                INSERT INTO public.scores(test_id, score_cookie, score_name, score_email, score_content, score_status, score_quest)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (test_id, user_session, "", "", "", "ACTIVO", 1))

        conn.commit()
        conn.close()
        return
    
    def get_test_by_id(self,test_id:int):
        conn, response = self._get_db_connection()
        if response:
            return response
        
        # Crear un cursor para ejecutar consultas
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT test_id, test_name, test_content
                FROM tests
                WHERE test_id = %s;
            """, (test_id,))
            test = cursor.fetchone()

        conn.close()
        return test
    
    def update_field_score(self,field:str, score_id:int, value:str):
        conn, response = self._get_db_connection()
        if response:
            return response
        
        with conn.cursor() as cursor:
            # Actualizar un campo específico en la tabla de scores
            cursor.execute(f"""
                UPDATE public.scores
                SET {field} = %s
                WHERE score_id = %s;
            """, (value, score_id))

        conn.commit()
        conn.close()
    
    def update_score_status(self, score_id:int,status:str):
        self.update_field_score('score_status', score_id, status)

    def update_score_content(self,string_content:str, score_id:int):
        self.update_field_score('score_content', score_id, string_content) 
    
    def update_score_quest(self, score_id:int):
        conn, response = self._get_db_connection()
        if response:
            return response

        with conn.cursor() as cursor:
            # Incrementar score_quest en la tabla de scores
            cursor.execute("""
                UPDATE public.scores
                SET score_quest = score_quest + 1
                WHERE score_id = %s;
            """, (score_id,))

        conn.commit()
        conn.close()