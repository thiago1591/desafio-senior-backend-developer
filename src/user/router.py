from fastapi import APIRouter, HTTPException, status
from typing import List
from . import schemas, service

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: schemas.UserCreate):
    return await service.create_user(user)

@router.get("/{user_id}", response_model=schemas.UserResponse)
async def get_user(user_id: int):
    return await service.get_user(user_id)

@router.get("/", response_model=List[schemas.UserResponse])
async def list_users(skip: int = 0, limit: int = 10):
    return await service.get_users(skip, limit)

@router.put("/{user_id}", response_model=schemas.UserResponse)
async def update_user(user_id: int, user: schemas.UserUpdate):
    return await service.update_user(user_id, user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    await service.delete_user(user_id)
    return None
