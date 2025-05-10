from typing import List, Optional
from pydantic import BaseModel

class ChatInput(BaseModel):
    message: str

class ChatbotResponse(BaseModel):
    message: str
    options: Optional[List[str]] = None 
    end_conversation: Optional[bool] = False