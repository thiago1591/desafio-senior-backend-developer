from fastapi import APIRouter
from src.user.router import router as user_router
from src.documents.router import router as document_router
from src.auth.router import router as auth_router

api_router = APIRouter()
api_router.include_router(user_router)
api_router.include_router(document_router)  
api_router.include_router(auth_router)  