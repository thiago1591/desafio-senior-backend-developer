from src.chatbot.models import ChatbotState

class CancelCardHandler:
    async def handle(self, state: ChatbotState, user_input: str) -> str:
        return "A solicitação de cancelamento do seu cartão foi criada. Verifique a sua caixa de e-mail"

cancel_card_handler = CancelCardHandler()
