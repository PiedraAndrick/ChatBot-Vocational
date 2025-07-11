from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

apikey = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=apikey)

def chat_openai(msg):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = [
            {
                "role": "system", 
                "content": "Eres un asistente universitario que se encarga de resolver dudas acerca del ingreso a las universidades en Ecuador, en especifico de la universidad de las fuerzas armadas ESPE de la sede santo domingo en la que se ofrece solo tres carreras, ingenieria en tecnologias de la informacion, ingenieria agropecuaria e ingenieria en biotecnologia"
            },
            {
                
                "role": "user",
                "content": msg
            }
        ],
        max_tokens=200
    )
    return response.choices[0].message.content
    
    
