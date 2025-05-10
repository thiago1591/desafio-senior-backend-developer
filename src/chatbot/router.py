from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from src.chatbot.services import intent_dispatcher
from src.user.models import User
from .schemas import ChatInput, ChatbotResponse
from .dependencies import parse_jwt_data
from src.chatbot import state_manager

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

@router.post("/start", response_model=ChatbotResponse)
async def start_conversation(token_data: dict = Depends(parse_jwt_data),):
    await state_manager.reset_state(token_data["user_id"])
    return ChatbotResponse(message="""
        Olá, eu sou o IPlani, o assistente virtual da Prefeitura. Como posso te ajudar hoje?

        1) Consultar saldo do meu cartão  
        2) Cancelar um cartão  
        3) Salvar um documento  
        4) Ver os documentos  
        5) Fazer uma pergunta
    """)

@router.post("/chat", response_model=ChatbotResponse)
async def chat(input: ChatInput, token_data: dict = Depends(parse_jwt_data)):
    state = await state_manager.get_or_create_state(token_data["user_id"])
    response_message = await intent_dispatcher.dispatch(state, input.message)
    return ChatbotResponse(message=response_message)