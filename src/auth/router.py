from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import UserLogin, UserLoginResponse, UserAuthenticated
from .service import login_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=UserLoginResponse)
async def login(user_login: UserLogin):
    return await login_user(user_login)