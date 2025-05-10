from src.chatbot.models import ChatbotState, IntentEnum
from src.chatbot.utils import format_user_input
from src.chatbot.services.intent_handlers.handle_check_balance import check_card_balance
from src.chatbot.services.intent_handlers.handle_question import answer_question_handler
from src.chatbot.services.intent_handlers.handle_find_my_documents import find_my_documents_handler
from src.chatbot.services.intent_handlers.handle_save_document import save_document_handler
from src.chatbot.services.intent_handlers.handle_cancel_card import cancel_card_handler

async def dispatch(state: ChatbotState, user_input: str) -> str:
    user_input = format_user_input(state.step, user_input)
    user = await state.user.first()
    
    if user_input == IntentEnum.CONSULTAR_SALDO:
        return await check_card_balance.handle(user.id)
    
    elif user_input == IntentEnum.VER_DOCUMENTOS:
        return await find_my_documents_handler.handle(user.id)
    
    elif user_input == IntentEnum.PERGUNTA_LIVRE or state.last_intent == IntentEnum.PERGUNTA_LIVRE:
        return await answer_question_handler.handle(state, user_input)
    
    elif user_input == IntentEnum.SALVAR_DOCUMENTO:
        return await save_document_handler.handle(state, user_input)
    
    elif user_input == IntentEnum.CANCELAR_CARTAO:
        return await cancel_card_handler.handle(state, user_input)
    
    else:
        return "Desculpe, não consegui identificar a ação. Digite o número com uma ação da lista."
