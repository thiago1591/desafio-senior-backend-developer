from src.chatbot.models import ChatbotState

class SaveDocumentHandler:
    async def handle(self, state: ChatbotState, user_input: str) -> str:
        return "Desculpe, esse serviço ainda não foi implementado"

save_document_handler = SaveDocumentHandler()
