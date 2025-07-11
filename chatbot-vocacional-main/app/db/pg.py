import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()

class ConexionPostgres:
    # Parámetros de conexión
    def __init__(self):
        self.conexion_params = {
            "host": os.getenv('DB_HOST'),
            "port": os.getenv('DB_PORT'),
            "database": os.getenv('DB_NAME'),
            "user": os.getenv('DB_USER'),
            "password": os.getenv('DB_PASS')
        }

    def connect(self):
        try:
            # Establecer la conexión
            conexion = psycopg2.connect(**self.conexion_params)
            return conexion, None  # Devuelve la conexión y None para indicar que no hay error
        except (Exception, psycopg2.Error) as error:
            return None, error  # Devuelve None para la conexión y el error
