from tortoise.exceptions import IntegrityError
from fastapi import HTTPException, status
from .models import User
from .schemas import UserResponse, UserUpdate
from datetime import datetime
from passlib.context import CryptContext
from opentelemetry import trace
from src.logging.logger import logger

from ..transport.service import create_transport_card

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

tracer = trace.get_tracer(__name__)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

async def create_user(user_create):
    logger.info(f"Iniciando criação de usuário: {user_create.email}")
    
    with tracer.start_as_current_span("create_user"):
        exists = await User.filter(cpf=user_create.cpf).exists() or \
                await User.filter(email=user_create.email).exists()

        if exists:
            logger.warning(f"Usuário já existe com CPF {user_create.cpf} ou email {user_create.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CPF ou e-mail já cadastrado."
        )
            
        try:
            user = await User.create(
                full_name=user_create.full_name,
                email=user_create.email,
                password=hash_password(user_create.password),
                birth_date=user_create.birth_date,
                cpf=user_create.cpf,
                phone=user_create.phone
            )
            logger.info(f"Usuário criado com sucesso: id={user.id}, email={user.email}")
            
            await create_transport_card(user.id)
            logger.info(f"Cartão de transporte criado para usuário id={user.id}")
            
            return UserResponse(
                id=user.id,
                full_name=user.full_name,
                email=user.email,
                birth_date=user.birth_date,
                cpf=user.cpf,
                phone=user.phone,
                created_at=str(user.created_at) if user.created_at else "",
                updated_at=str(user.updated_at) if user.updated_at else ""
            )
        except IntegrityError as e:
            logger.error(f"Erro de integridade ao criar usuário: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro de integridade ao criar usuário."
            )

async def get_user(user_id: int):
    user = await User.filter(id=user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )
    return UserResponse(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        birth_date=user.birth_date,
        cpf=user.cpf,
        phone=user.phone,
        created_at=str(user.created_at) if user.created_at else None,
        updated_at=str(user.updated_at) if user.updated_at else None
    )

async def get_users(skip: int = 0, limit: int = 10):
    users = await User.all().offset(skip).limit(limit)
    return [
        UserResponse(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            birth_date=user.birth_date,
            cpf=user.cpf,
            phone=user.phone,
            created_at=str(user.created_at) if user.created_at else None,
            updated_at=str(user.updated_at) if user.updated_at else None
        )
        for user in users
    ]

async def update_user(user_id: int, user_update: UserUpdate):
    user = await User.filter(id=user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )
    
    if user_update.full_name:
        user.full_name = user_update.full_name
    if user_update.email:
        user.email = user_update.email
    if user_update.birth_date:
        user.birth_date = user_update.birth_date
    if user_update.cpf:
        user.cpf = user_update.cpf
    if user_update.phone:
        user.phone = user_update.phone
    
    user.updated_at = datetime.utcnow() 
    await user.save()

    return UserResponse(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        birth_date=user.birth_date,
        cpf=user.cpf,
        phone=user.phone,
        created_at=str(user.created_at) if user.created_at else "",
        updated_at=str(user.updated_at) if user.updated_at else ""
    )

async def delete_user(user_id: int):
    user = await User.filter(id=user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )
    
    await user.delete()
    return {"detail": "Usuário excluído com sucesso."}
