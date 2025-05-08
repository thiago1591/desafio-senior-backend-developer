from fastapi import APIRouter
from .schemas import UserLogin, UserLoginResponse
from .service import login_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=UserLoginResponse)
async def login(user_login: UserLogin):
    return await login_user(user_login)