from src.chatbot.models import ChatbotState, IntentEnum
from src.chatbot.utils import get_mock_questions, match_question

class AnswerQuestionHandler:
    async def handle(self, state: ChatbotState, user_input: str) -> str:
        if state.step == 0:
            state.step = 1
            state.last_intent = IntentEnum.PERGUNTA_LIVRE
            await state.save()
            return "Qual é a sua dúvida?"
        
        state.step = 0
        state.last_intent = None
        state.context = None
        await state.save()
        
        resposta = match_question(user_input, get_mock_questions())

        if resposta:
            return resposta

        return "Desculpe, não tenho uma resposta para essa pergunta no momento. Tente outra pergunta."

answer_question_handler = AnswerQuestionHandler()
