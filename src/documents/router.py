from fastapi import APIRouter, Depends, status
from typing import List

from src.documents.exceptions import UserNotOwner
from . import schemas, service
from .dependencies import parse_jwt_data, valid_owned_document

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/", response_model=schemas.DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(
    document: schemas.DocumentBase,
    token_data: dict = Depends(parse_jwt_data),
):
    document_with_user_id = schemas.DocumentCreate(
        **document.model_dump(),
        user_id=token_data["user_id"]
    )
    return await service.create_document(document_with_user_id)
@router.get("/", response_model=List[schemas.DocumentResponse])
async def list_documents(
    skip: int = 0,
    limit: int = 10,
    token_data: dict = Depends(parse_jwt_data)
):
    return await service.get_documents(skip, limit)


@router.get("/{document_id}", response_model=schemas.DocumentResponse)
async def get_document(
    document = Depends(valid_owned_document)
):
    return await service._to_document_response(document)


@router.put("/{document_id}", response_model=schemas.DocumentResponse)
async def update_document(
    document_id: int,
    update: schemas.DocumentUpdate,
    document = Depends(valid_owned_document),
):
    return await service.update_document(document_id, update)


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document = Depends(valid_owned_document),
):
    await service.delete_document(document.id)
    return None
