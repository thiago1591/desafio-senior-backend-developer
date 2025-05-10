from src.chatbot.models import ChatbotState
from src.transport import service
from src.transport.dependencies import get_card_by_number_or_404

class CheckBalanceHandler:
    async def handle(self, user_id: int) -> str:
        cards = await service.get_user_cards(user_id)
        
        if not cards:
            return "Você não tem cartões cadastrados"
        
        if len(cards) == 1:
            card = await get_card_by_number_or_404(cards[0].card_number)
            convertedMoney = card.balance / 100 
            return f"Seu saldo atual é: R$ {convertedMoney:.2f}"
        
        resposta = "Seus saldos são:\n"
        for card_info in cards:
            card = await get_card_by_number_or_404(card_info.card_number)
            final = card.card_number[-4:]
            convertedMoney = card.balance / 100 
            resposta += f"- Cartão final {final}: R$ {convertedMoney:.2f}\n"
        
        return resposta.strip()

check_card_balance = CheckBalanceHandler()
