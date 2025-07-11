from app.services.test import TestService
from app.services.flow import FlowService
from app.utils.clavesHandle import CARRERAS, RESPUESTAS_NEGATIVAS,MALLA,PERFIL,INFO,AREAS,CARRERAS_RELACIONADAS
from app.utils.emailHandle import EmailSender
from app.utils.templateTestAnswer import templateTest, templateTest2
import json
import spacy

class TestController:

    #CONTRUCTOR
    def __init__(self):
        # Cargar el modelo de lenguaje de spaCy
        self.nlp = spacy.load("es_core_news_md")
        self.testSrv = TestService()
        self.flowSrv = FlowService()

    def start_test(self,userSession:str,test_id:int):

        #INSERTAR REGISTRO QUE INICIA DEL TEST
        self.testSrv.start_test(userSession,test_id)

        #OBTENER LA PRIMERA PREGUNTA DEL TEST
        test = self.testSrv.get_test_by_id(test_id)
        test_content = json.loads(test[2])
            
        res = {"status": "OK","data": []}
        first_question = test_content[0]
        for cont in first_question["contenido"]:
            res["data"].append({
                "message": cont["texto"],
                "tipo":"MENSAJE" if cont["tipo"] == 'info' else "TEST",
                "contenido": None
        })
        return res
    
    def score_test(self,user_score:dict,user_text:list[str]):
        test_id = user_score[0][3]
        score_id = user_score[0][0]
        scoring = {} if user_score[0][4].strip() == "" else json.loads(user_score[0][4])
        question_number  = user_score[0][2]
        user_name = user_score[0][5]
        user_email = user_score[0][6]
        
        #verificar si es un respuesta negativa
        negative_response = self.cancel_test(user_text[0],score_id)
        if negative_response is not None: return negative_response
        
        test = self.testSrv.get_test_by_id(test_id)
        test_content = json.loads(test[2])
        
        current_question  = next((q for q in test_content if q.get("pregunta") == question_number), None)

        for content  in current_question["contenido"]:
            # Procesar contenido informativo
            if content["tipo"] == "info": continue
            
            # Procesar campo
            if content["tipo"] == "campo": 
                self.testSrv.update_field_score(content["campo"],score_id,user_text[0])
                
            # Procesar puntaje
            if content["tipo"] == "puntaje": 
                user_doc  = self.nlp(user_text[0].lower())
                option_doc  = self.nlp(content["texto"].lower())
                similarity = user_doc.similarity(option_doc )   
                if similarity  >= 0.9:
                    scoring[content["puntaje"]] = scoring.get(content["puntaje"], 0) + 1
                    score_content  = json.dumps(scoring)
                    self.testSrv.update_score_content(score_content ,score_id)
            
            # Procesar opción múltiple
            if content["tipo"] == "opcionmultiple":
                for i in range(int(content["limite"])):
                        
                    for sub_content  in content["contenido"]:
                        user_doc  = self.nlp(user_text[i].lower())
                        option_doc  = self.nlp(sub_content ["texto"].lower())
                        similarity  = user_doc.similarity(option_doc )
                        if similarity  >= 0.9:
                            scoring[sub_content["puntaje"]] = scoring.get(sub_content["puntaje"], 0) + 1
                            score_content  = json.dumps(scoring)
                            self.testSrv.update_score_content(score_content ,score_id)
        
        #ACTUALIZAR EL NUMERO DE PREGUNTA DEL TEST
        self.testSrv.update_score_quest(score_id)
        
        next_quesstion = next((q for q in test_content if q.get("pregunta") == (question_number+1)), None)
        response  = {"status": "OK","data": []}     

        #VERIFICAR SI YA FINALIZO EL TEST
        if next_quesstion is not None:
            for content  in next_quesstion["contenido"]:
                response_content = {
                    "message": content["texto"],
                    "tipo": "MENSAJE" if content["tipo"] == 'info' else "TEST",
                    "contenido": content.get("contenido") if content["tipo"] == 'opcionmultiple' else None
                }
                if content["tipo"] == 'opcionmultiple':
                    response_content["limite"] = content["limite"]
                    response_content["tipo"] = "OPCIONMULTIPLE",
                response["data"].append(response_content)
                                        
            return response 
        
        #ACTUALIZAR ESTADO DE LA PREGUNTA
        self.testSrv.update_score_status(score_id,'FINALIZADO')

        #ENVIAR CORREO CON LA INFORMACION
        email_sender = EmailSender()

        sorted_keys = sorted(scoring, key=scoring.get, reverse=True)
        second_max_key = sorted_keys[1] if len(sorted_keys) >= 2 else None
        if second_max_key is not None:
            res_email = email_sender.send_email(
             subject="Orientacion vocacional",
             html=templateTest2(
                 INFO[max(scoring, key=scoring.get)],
                 PERFIL[max(scoring, key=scoring.get)],
                 user_name,
                 INFO[second_max_key],
                 PERFIL[second_max_key],
             ),
             to_address=user_email,
             receiver_username=user_name,
             attachment_path= [
                 f"app/public/pdf/mallas/{MALLA[max(scoring, key=scoring.get)]}",
                 f"app/public/pdf/mallas/{MALLA[second_max_key]}"]
            )
            response["data"].extend([
                {"message": "(Preparando tu recomendación en 3️⃣, 2️⃣, 1️⃣) 🥁", "tipo": "MENSAJE", "contenido": None},
                {"message": "Enhorabuena, analice tu perfil y según mis resultados muestran que puedes escoger:", "tipo": "MENSAJE", "contenido": None},
                {"message": f"ÁREA RECOMENDADA: {AREAS[max(scoring, key=scoring.get)]}", "tipo": "MENSAJE", "contenido": None},
                {"message": f"Carreras: {CARRERAS_RELACIONADAS[max(scoring, key=scoring.get)]}", "tipo": "MENSAJE", "contenido": None},
                {"message": f"Una de las mejores opciones es: {CARRERAS[max(scoring, key=scoring.get)]} 🎉🎊", "tipo": "MENSAJE", "contenido": None},
                {"message": f"ÁREA RECOMENDADA: {AREAS[second_max_key]}", "tipo": "MENSAJE", "contenido": None},
                {"message": f"Carreras: {CARRERAS_RELACIONADAS[second_max_key]}", "tipo": "MENSAJE", "contenido": None},
                {"message": f"Una de las mejores opciones es: {CARRERAS[second_max_key]} 🎉🎊", "tipo": "MENSAJE", "contenido": None},
                {"message": "Toda la información correspondiente a malla curricular y perfil de egreso te la envie a tu correo. ¡¡Disfrutalo!!. ¿Te puedo ayudar en algo más?", "tipo": "MENSAJE", "contenido": None}
            ])
            return response 
        
        res_email = email_sender.send_email(
             subject="Orientacion vocacional",
             html=templateTest(INFO[max(scoring, key=scoring.get)],PERFIL[max(scoring, key=scoring.get)],user_name),
             to_address=user_email,
             receiver_username=user_name,
             attachment_path= f"app/public/pdf/mallas/{MALLA[max(scoring, key=scoring.get)]}"
        )  
        response["data"].extend([
            {"message": "(Preparando tu recomendación en 3️⃣, 2️⃣, 1️⃣) 🥁", "tipo": "MENSAJE", "contenido": None},
            {"message": "Enhorabuena, analice tu perfil y según mis resultados muestran que puedes escoger:", "tipo": "MENSAJE", "contenido": None},
            {"message": f"ÁREA RECOMENDADA: {AREAS[max(scoring, key=scoring.get)]}", "tipo": "MENSAJE", "contenido": None},
            {"message": f"Carreras: {CARRERAS_RELACIONADAS[max(scoring, key=scoring.get)]}", "tipo": "MENSAJE", "contenido": None},
            {"message": f"Una de las mejores opciones es: {CARRERAS[max(scoring, key=scoring.get)]} 🎉🎊", "tipo": "MENSAJE", "contenido": None},
            {"message": "Toda la información correspondiente a malla curricular y perfil de egreso te la envie a tu correo. ¡¡Disfrutalo!!. ¿Te puedo ayudar en algo más?", "tipo": "MENSAJE", "contenido": None}
        ])

        return response 

    def cancel_test(self,user_answer:str,score_id:int):
        user_doc = self.nlp(user_answer.lower())
        
        response = {"status": "OK","data": []}
        
        for answer in RESPUESTAS_NEGATIVAS:
            answer_doc = self.nlp(answer)
            similarity = user_doc.similarity(answer_doc)
            
            if similarity  >= 0.9:

                self.testSrv.update_score_status(score_id,'FINALIZADO')
                response["data"].append({
                    "message": "Upps hubiese deseado poder ayudarte con tu sugerencia, es necesario que hagas el test para poder ayudarte. Puedes volver cuando quieras.",
                    "tipo":"MENSAJE",
                    "contenido": None
                })
                return response
        return None  
        