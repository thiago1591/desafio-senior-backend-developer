from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.user.router import router as user_router
from src.documents.router import router as document_router
from src.auth.router import router as auth_router
from src.transport.router import router as transport_router
from src.forgot_password.router import router as forgot_password_router
from src.chatbot.router import router as chatbot_router

api_router = APIRouter()

@api_router.get("/health", response_class=JSONResponse)
async def health_check():
    return JSONResponse(content={"status": "ok"}, status_code=200)

api_router.include_router(user_router)
api_router.include_router(document_router)  
api_router.include_router(auth_router)  
api_router.include_router(transport_router)
api_router.include_router(forgot_password_router)
api_router.include_router(chatbot_router)