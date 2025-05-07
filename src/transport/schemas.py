from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class TransportCardBase(BaseModel):
    balance: int = Field(..., example=5000) 
    card_number: str = Field(..., example="1234567890")
    status: str = Field(..., example="active")  


class TransportCardCreate(TransportCardBase):
    user_id: int


class TransportCardUpdate(BaseModel):
    balance: Optional[int] = None
    status: Optional[str] = None


class TransportCardResponse(TransportCardBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class RechargeRequest(BaseModel):
    amount: int = Field(..., example=1000) 

    class Config:
        orm_mode = True
        
class TransportCardRecharge(BaseModel):
    amount: int = Field(..., example=1000)  

    class Config:
        orm_mode = True
        
class TransportCardDebit(BaseModel):
    amount: int = Field(..., example=1000) 

    class Config:
        orm_mode = True

class TransportTransactionHistoryResponse(BaseModel):
    id: int
    card_number: str = Field(..., example="1234567890")
    transaction_type: str = Field(..., example="recharge") 
    amount: int = Field(..., example=1000)  
    balance_after_transaction: int = Field(..., example=5000) 
    transaction_date: datetime 

    class Config:
        orm_mode = True