import random
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from tortoise.exceptions import DoesNotExist
from src.forgot_password.models import PasswordRecovery
from src.user.models import User
from src.forgot_password.utils import send_email 
from src.forgot_password.schemas import ForgotPasswordRequest
from src.auth.service import create_access_token
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def send_recovery_code(data: ForgotPasswordRequest):
    try:
        user = await User.get(email=data.email)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )
    recovery_code = str(random.randint(10000, 99999))
    recovery_code_expiration = datetime.now(timezone.utc) + timedelta(hours=1)

    await PasswordRecovery.create(
            user=user,
            recovery_code=recovery_code,
            recovery_code_expiration=recovery_code_expiration
    )
    is_sent = await send_email(
        subject="Recuperação de senha",
        recipient_email=user.email,
        body=f"TextGrader - Seu código para recuperação da senha é {recovery_code}"
    )
    if not is_sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao enviar e-mail."
        )
    return {"response": f"para fins de simulação, o código é retornado aqui. o código é : ${recovery_code}"}

async def verify_recovery_code(email: str, code: str):
    if not email or not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email e código são obrigatórios."
        )

    user = await User.get_or_none(email=email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )

    if not user.recovery_code or not user.recovery_code_expiration:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum código de recuperação solicitado."
        )

    expiration = user.recovery_code_expiration
    if expiration.tzinfo is None:
        expiration = expiration.replace(tzinfo=timezone.utc)

    if datetime.now(timezone.utc) > expiration:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O código expirou."
        )

    if code != user.recovery_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Código inválido."
        )

    user.recovery_code = None
    user.recovery_code_expiration = None
    await user.save()

    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(hours=1))

    return {"access_token": access_token}

async def reset_password(user_id: int, new_password: str):
    if not new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nova senha é obrigatória."
        )

    user = await User.get_or_none(id=user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )

    hashed_password = pwd_context.hash(new_password)

    user.password = hashed_password
    await user.save()

    return {"status": "Senha atualizada com sucesso"}
