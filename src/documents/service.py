from fastapi import HTTPException, status
from tortoise.exceptions import DoesNotExist, IntegrityError
from .models import Document
from .schemas import DocumentCreate, DocumentUpdate, DocumentResponse

# Criar documento
async def create_document(document: DocumentCreate):
    try:
        doc = await Document.create(
            user_id=document.user_id,
            document_type=document.document_type,
            file_path=document.file_path,
            file_name=document.file_name,
            document_number=document.document_number
        )
        return await _to_document_response(doc)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Documento deste tipo já existe para o usuário."
        )

# Listar documentos
async def get_documents(skip: int = 0, limit: int = 10):
    documents = await Document.all().offset(skip).limit(limit).prefetch_related("user")
    return [await _to_document_response(doc) for doc in documents]

# Obter documento por ID
async def get_document(document_id: int):
    doc = await Document.filter(id=document_id).first()
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado."
        )
    return await _to_document_response(doc)

# Atualizar documento
async def update_document(document_id: int, update: DocumentUpdate):
    doc = await Document.filter(id=document_id).first()
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado."
        )

    if update.document_type is not None:
        doc.document_type = update.document_type
    if update.file_path is not None:
        doc.file_path = update.file_path
    if update.file_name is not None:
        doc.file_name = update.file_name
    if update.document_number is not None:
        doc.document_number = update.document_number

    await doc.save()
    return await _to_document_response(doc)

# Deletar documento
async def delete_document(document_id: int):
    doc = await Document.filter(id=document_id).first()
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado."
        )
    await doc.delete()

# Conversor auxiliar
async def _to_document_response(doc: Document) -> DocumentResponse:
    return DocumentResponse(
        id=doc.id,
        user_id=doc.user_id,
        document_type=doc.document_type,
        file_path=doc.file_path,
        file_name=doc.file_name,
        document_number=doc.document_number,
        uploaded_at=str(doc.uploaded_at)
    )
