from fastapi import APIRouter, Depends, HTTPException
from src.forgot_password.dependencies import parse_jwt_data
from src.forgot_password.schemas import ForgotPasswordRequest, ResetPasswordRequest, VerifyCodeRequest
from src.forgot_password import service

router = APIRouter(prefix="/forgot-password", tags=["password-recovery"])

@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest):
    try:
        return await service.send_recovery_code(request) 
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/verify-code")
async def verify_code(request: VerifyCodeRequest):
    try:
        token = await service.verify_recovery_code(request.email, request.code)
        return {"access_token": token}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset-password")
async def reset_password_route(
    request: ResetPasswordRequest,
    token_data: dict = Depends(parse_jwt_data),
):
    try:
        user_id = token_data["user_id"]
        await service.reset_password(user_id, request.new_password)
        return {"status": "Senha atualizada com sucesso"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))