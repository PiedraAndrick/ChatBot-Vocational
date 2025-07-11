import ollama

# Definir el archivo del modelo
modelfile = '''
FROM llama2
SYSTEM eres un asistente de ayuda universitaria
'''

# Crear el modelo
ollama.create(model='asistente', modelfile=modelfile)

# Realizar una consulta al modelo
def responseOllama(message):
    response = ollama.chat(model='asistente', messages=[
        {
            'role': 'user',
            'content': message
        }
    ])
    return response




# Imprimir la respuesta
response = responseOllama('que es la universidad')
print(response['message']['content'])
