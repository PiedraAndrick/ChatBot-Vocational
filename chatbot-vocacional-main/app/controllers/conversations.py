from app.utils.datesHandle import get_formatted_date
from app.services.conversations import ConversationService

class ConversationController:
        #CONTRUCTOR
    def __init__(self):
        self.convSrv = ConversationService()
    
    def save_conversation(self,user_session:str,messages:list[str],emitter:str):
        if emitter == 'USUARIO':
            for message in messages:
                self.convSrv.save_conversation(user_session,message,emitter,get_formatted_date())
        if emitter == 'BOT' :
            for message in messages:
                msj = message["message"]
                self.convSrv.save_conversation(user_session,msj,emitter,get_formatted_date())
        return