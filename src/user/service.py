from tortoise.exceptions import IntegrityError
from fastapi import HTTPException, status
from .models import User
from .schemas import UserResponse, UserUpdate
from datetime import datetime

async def create_user(user_create):
    exists = await User.filter(username=user_create.username).exists() or \
             await User.filter(email=user_create.email).exists()
    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário ou e-mail já cadastrado."
        )
    try:
        user = await User.create(
            username=user_create.username,
            email=user_create.email,
            password=user_create.password,  # Em produção, faça hash!
            birth_date=user_create.birth_date,
            cpf=user_create.cpf,
            phone=user_create.phone
        )
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            birth_date=user.birth_date,
            cpf=user.cpf,
            phone=user.phone,
            created_at=str(user.created_at) if user.created_at else None,
            updated_at=str(user.updated_at) if user.updated_at else None
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro de integridade ao criar usuário."
        )

# Função para pegar um usuário pelo ID
async def get_user(user_id: int):
    user = await User.filter(id=user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )
    return UserResponse(
        id=user.id,
        username=user.username,
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
            username=user.username,
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
    
    if user_update.username:
        user.username = user_update.username
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
        username=user.username,
        email=user.email,
        birth_date=user.birth_date,
        cpf=user.cpf,
        phone=user.phone,
        created_at=str(user.created_at) if user.created_at else None,
        updated_at=str(user.updated_at) if user.updated_at else None
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
