from src.chatbot.models import ChatbotState

async def get_or_create_state(user_id: int) -> ChatbotState:
    state = await ChatbotState.filter(user_id=user_id).first()
    if not state:
        state = await ChatbotState.create(user_id=user_id, step=0, context={})
    return state

async def reset_state(user_id: int):
    await ChatbotState.filter(user_id=user_id).delete()
