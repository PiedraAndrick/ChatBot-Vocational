from app.db.pg import ConexionPostgres
from app.services.questions import QuestioService
from app.services.answers import AnswerService 
from app.controllers.test import TestController
from app.services.test import TestService
from app.services.flow import FlowService
from app.utils.clavesHandle import RESPUESTAS_NEGATIVAS, RESPUESTAS_POSITIVAS
from app.utils.openaiHandle import chat_openai
import json
import spacy
import re
from unidecode import unidecode

class ChatController:


    def __init__(self):
        # Cargar el modelo de lenguaje de spaCy
        self.nlp = spacy.load("es_core_news_md")
        self.conexion_pg = ConexionPostgres()
        self.srvAnnswer = AnswerService()
        self.srvQuestion = QuestioService()
        self.ctrTest = TestController()
        self.srvTest = TestService()
        self.srvFlow= FlowService()
    ''' 
        METODO INICIO DE LA CONEVERSACION
    '''
    def start_chat(self):
        
        res = {"status": "OK","data": []}
        #OBTENER TODOS LOS FLUJOS
        flujos = self.srvFlow.get_flows()
        for flujo in flujos:
            res["data"].append({
                "message": flujo[0]
            })
        return res

    ''' 
        METODO CHAT
    ''' 
    def chat_flujo(self, prompt,userSession):
      
        #VERIFICAR SI SE ENCUENTRA DENTRO DE UN TEST
        user_score = self.srvTest.check_test(userSession)
        if len(user_score) > 0:
            #PUNTUAR LAS RESPUESTAS DEL TEST
            res = self.ctrTest.score_test(user_score,prompt.text)
            return res
            
        #OBTENER TODAS LAS PREGUNTAS
        opciones = self.srvQuestion.get_questions()
        mejor_similitud = 0
        mejor_indice = -1
        test_id = 0
        verificar_test= False

        # Procesar la entrada del usuario
        
        texto_sin_acentos = unidecode(prompt.text[0].lower())
        texto_limpio = re.sub(r'[^a-zA-Z0-9\s]', '', texto_sin_acentos)
        doc_usuario = self.nlp(texto_limpio)

        #verificar si es un respuesta negativa
        negative_response = self.negative_chat(doc_usuario)
        if negative_response is not None: return negative_response

        #verificar si es un respuesta afirmativa
        afirmative_response = self.afirmative_chat(doc_usuario)
        if afirmative_response is not None: return afirmative_response
        
        for i, opcion in enumerate(opciones):
            # Procesar la opción
            texto_sin_acentos = unidecode(opcion[2])
            texto_limpio = re.sub(r'[^a-zA-Z0-9\s]', '', texto_sin_acentos)
            doc_opcion = self.nlp(texto_limpio)
            
            # Calcular la similitud entre la entrada del usuario y la opción
  
            similitud = doc_usuario.similarity(doc_opcion)

            # Actualizar el mejor índice si se encuentra una similitud más alta 0 - 1
            if similitud > mejor_similitud:
                mejor_similitud = similitud
                mejor_indice = opcion[0]
                verificar_test= opcion[3]
                test_id = opcion[4]
                
        #VERIFICAMOS QUE TIPO DE RESPUESTAS SE RETORNA
        if verificar_test:
            res = self.ctrTest.start_test(userSession,test_id)
            return res
            
        #Obtener las respuestas de la pregunta     
        if mejor_similitud <0.6:
            msg = chat_openai(prompt.text[0].lower())
            res = {"status": "OK","data": [{
                "message": msg,
                "tipo":"MENSAJE",
                "contenido": None
            }]}    
            return res
            
        respuestas = self.srvAnnswer.get_answers_by_quetion(mejor_indice)

        res = {"status": "OK","data": []}
        for resp in respuestas:
            contenido = None
            if resp[4] is not None : contenido = json.loads(resp[4])
            res["data"].append({
                "message": resp[2],
                "tipo":resp[3],
                "contenido": contenido
            })
        return res


    ''' 
        METODO INICIO DE LA CONEVERSACION
    '''
    def negative_chat(self, user_doc):
        response = {"status": "OK","data": []}
        for answer in RESPUESTAS_NEGATIVAS:
            texto_sin_acentos = unidecode(answer)
            texto_limpio = re.sub(r'[^a-zA-Z0-9\s]', '', texto_sin_acentos)
            answer_doc = self.nlp(texto_limpio)
            similarity = user_doc.similarity(answer_doc)
            if similarity  >= 0.9:
                response["data"].append({
                    "message": "Upps hubiese deseado poder ayudarte con tu sugerencia.",
                    "tipo":"MENSAJE",
                    "contenido": None
                })
                
                return response
        return None
    
    def afirmative_chat(self, user_doc):
        response = {"status": "OK","data": []}
        for answer in RESPUESTAS_POSITIVAS:
            texto_sin_acentos = unidecode(answer)
            texto_limpio = re.sub(r'[^a-zA-Z0-9\s]', '', texto_sin_acentos)
            
            answer_doc = self.nlp(texto_limpio)
            similarity = user_doc.similarity(answer_doc)
            if similarity  >= 0.9:
                response["data"].append({
                    "message": "Sobre que quieres hablar",
                    "tipo":"MENSAJE",
                    "contenido": None
                })
                flujos = self.srvFlow.get_flows()
                for flujo in flujos:
                    response["data"].append({
                        "message": flujo[0],
                        "tipo":"MENSAJE",
                        "contenido": None
                    })
                    
                return response
        return None