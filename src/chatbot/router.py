from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from .schemas import ChatbotResponse, InteractionRequest
from .dependencies import parse_jwt_data
from src.chatbot import service

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

@router.get("/start", response_model=ChatbotResponse)
async def start_conversation(
    token_data: dict = Depends(parse_jwt_data)
):
    return await service.start_conversation(token_data["user_id"])

@router.post("/interact", response_model=ChatbotResponse)
async def handle_interaction(
    interaction_request: InteractionRequest
):
    return await service.handle_interaction(
        interaction_request.chat_id,
        interaction_request.user_selection,
        interaction_request.node_id
    )

@router.post("/reset", response_model=ChatbotResponse)
async def reset_conversation(
    user_id: int
):
    """
    Reset the conversation state for a user
    """