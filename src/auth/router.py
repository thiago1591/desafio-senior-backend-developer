from http.client import HTTPException
import re
from starlette.status import HTTP_400_BAD_REQUEST
from fastapi import APIRouter, Form, Request
from src.auth.utils import is_valid_cpf
from .schemas import UserLogin, UserLoginResponse
from .service import login_user
from src.config import auth_settings 
from fastapi.responses import RedirectResponse
import httpx

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=UserLoginResponse)
async def login(
    username: str = Form(...),
    password: str = Form(...)
):
    #validações aqui na rota (fora da camada de schema) para funcionar com o botão de autenticação do swagger
    if not is_valid_cpf(username):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="CPF inválido.")

    if len(password) < 8:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="A senha deve ter pelo menos 8 caracteres.")
    if not re.search(r'[A-Z]', password):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="A senha deve conter pelo menos uma letra maiúscula.")
    if not re.search(r'[0-9]', password):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="A senha deve conter pelo menos um número.")
    
    user_login = UserLogin(username=username, password=password)
    return await login_user(user_login)

@router.get("/google/login")
async def google_login():
    redirect_uri = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={auth_settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={auth_settings.GOOGLE_REDIRECT_URI}"
        "&response_type=code"
        "&scope=openid%20email%20profile"
    )
    return RedirectResponse(redirect_uri)

@router.get("/google/callback")
async def google_callback(request: Request):
    code = request.query_params.get("code")

    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": auth_settings.GOOGLE_CLIENT_ID,
                "client_secret": auth_settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": auth_settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        token_data = token_resp.json()
        access_token = token_data.get("access_token")

        user_resp = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile = user_resp.json()

    return profile  

@router.get("/meta/login")
async def meta_login():
    redirect_uri = (
        "https://www.facebook.com/v18.0/dialog/oauth"
        f"?client_id={auth_settings.META_CLIENT_ID}"
        f"&redirect_uri={auth_settings.META_REDIRECT_URI}"
        "&scope=email,public_profile"
        "&response_type=code"
    )
    return RedirectResponse(redirect_uri)

@router.get("/meta/callback")
async def meta_callback(request: Request):
    code = request.query_params.get("code")

    async with httpx.AsyncClient() as client:
        token_resp = await client.get(
            "https://graph.facebook.com/v18.0/oauth/access_token",
            params={
                "client_id": auth_settings.META_CLIENT_ID,
                "redirect_uri": auth_settings.META_REDIRECT_URI,
                "client_secret": auth_settings.META_CLIENT_SECRET,
                "code": code,
            },
        )
        token_data = token_resp.json()
        access_token = token_data.get("access_token")

        user_resp = await client.get(
            "https://graph.facebook.com/me",
            params={"fields": "id,name,email", "access_token": access_token},
        )
        profile = user_resp.json()

    return profile
