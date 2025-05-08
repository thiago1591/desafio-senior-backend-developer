from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class ChatbotResponse(BaseModel):
    chat_id: int
    message: str
    options: List[str]
    node_id: Optional[str] = None

class InteractionRequest(BaseModel):
    chat_id: int
    user_selection: str
    node_id: Optional[str] = None

class ChatSessionResponse(BaseModel):
    id: int
    user_id: int
    current_node_id: str
    created_at: datetime
    last_interaction_at: datetime
    is_active: bool

    class Config:
        orm_mode = True

class ChatInteractionResponse(BaseModel):
    id: int
    chat_session_id: int
    node_id: str
    user_selection: str
    created_at: datetime

    class Config:
        orm_mode = True

class ChatbotNodeResponse(BaseModel):
    id: str
    parent_id: Optional[str] = None
    type: str
    message: str
    options: List[dict] = []

    class Config:
        orm_mode = True
