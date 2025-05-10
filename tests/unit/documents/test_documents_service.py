from fastapi import HTTPException, status
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.documents.models import Document
from src.documents.service import create_document, delete_document, get_document, get_documents, update_document
from src.documents.schemas import DocumentCreate, DocumentUpdate


@pytest.mark.asyncio
@pytest.mark.unit
@patch("src.documents.service._to_document_response", new_callable=AsyncMock)
@patch("src.documents.service.Document.create", new_callable=AsyncMock)
async def test_create_document_success(mock_create, mock_to_response):
    document_data = DocumentCreate(
        user_id=1,
        document_type="RG",
        file_path="/uploads/docs/rg123.pdf",
        file_name="rg123.pdf",
        document_number="123456789"
    )

    mock_doc = MagicMock()
    mock_create.return_value = mock_doc

    expected_response = {"mocked": "response"}
    mock_to_response.return_value = expected_response

    result = await create_document(document_data)

    mock_create.assert_awaited_once_with(
        user_id=1,
        document_type="RG",
        file_path="/uploads/docs/rg123.pdf",
        file_name="rg123.pdf",
        document_number="123456789"
    )
    mock_to_response.assert_awaited_once_with(mock_doc)
    assert result == expected_response

 
@pytest.mark.asyncio
@pytest.mark.unit
@patch("src.documents.service._to_document_response", new_callable=AsyncMock)
@patch("src.documents.service.Document.filter", new_callable=MagicMock)
async def test_get_document_success(mock_filter, mock_to_response):
    mock_doc = MagicMock()
    mock_filter.return_value.first = AsyncMock(return_value=mock_doc)

    expected_response = {"mocked": "document response"}
    mock_to_response.return_value = expected_response

    result = await get_document(document_id=1)

    mock_filter.assert_called_once_with(id=1)
    mock_filter.return_value.first.assert_awaited_once()
    mock_to_response.assert_awaited_once_with(mock_doc)
    assert result == expected_response

@pytest.mark.asyncio
@pytest.mark.unit
@patch("src.documents.service.Document.filter", new_callable=MagicMock)
async def test_get_document_not_found(mock_filter):
    mock_filter.return_value.first = AsyncMock(return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        await get_document(document_id=999)

    mock_filter.assert_called_once_with(id=999)
    mock_filter.return_value.first.assert_awaited_once()
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Documento não encontrado."
    
    
@pytest.mark.asyncio
@pytest.mark.unit
@patch("src.documents.service._to_document_response", new_callable=AsyncMock)
@patch("src.documents.service.Document.filter", new_callable=MagicMock)
async def test_update_document_success(mock_filter, mock_to_response):
    mock_doc = MagicMock()
    mock_doc.save = AsyncMock()
    mock_filter.return_value.first = AsyncMock(return_value=mock_doc)

    update_data = DocumentUpdate(
        document_type="CNH",
        file_path="/docs/cnh456.pdf",
        file_name="cnh456.pdf",
        document_number="987654321"
    )

    expected_response = {"mocked": "updated_document"}
    mock_to_response.return_value = expected_response

    result = await update_document(document_id=1, update=update_data)

    mock_filter.assert_called_once_with(id=1)
    mock_filter.return_value.first.assert_awaited_once()
    mock_doc.save.assert_awaited_once()
    mock_to_response.assert_awaited_once_with(mock_doc)

    assert mock_doc.document_type == "CNH"
    assert mock_doc.file_path == "/docs/cnh456.pdf"
    assert mock_doc.file_name == "cnh456.pdf"
    assert mock_doc.document_number == "987654321"
    assert result == expected_response

@pytest.mark.asyncio
@pytest.mark.unit
@patch("src.documents.service.Document.filter", new_callable=MagicMock)
async def test_update_document_not_found(mock_filter):
    mock_filter.return_value.first = AsyncMock(return_value=None)

    update_data = DocumentUpdate(document_type="RG")

    with pytest.raises(HTTPException) as exc_info:
        await update_document(document_id=999, update=update_data)

    mock_filter.assert_called_once_with(id=999)
    mock_filter.return_value.first.assert_awaited_once()
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Documento não encontrado."
    
@pytest.mark.asyncio
@pytest.mark.unit
@patch("src.documents.service.Document.filter", new_callable=MagicMock)
async def test_delete_document_success(mock_filter):
    mock_doc = MagicMock()
    mock_doc.delete = AsyncMock()
    mock_filter.return_value.first = AsyncMock(return_value=mock_doc)

    await delete_document(document_id=1)

    mock_filter.assert_called_once_with(id=1)
    mock_filter.return_value.first.assert_awaited_once()
    mock_doc.delete.assert_awaited_once()

@pytest.mark.asyncio
@pytest.mark.unit
@patch("src.documents.service.Document.filter", new_callable=MagicMock)
async def test_delete_document_not_found(mock_filter):
    mock_filter.return_value.first = AsyncMock(return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        await delete_document(document_id=999)

    mock_filter.assert_called_once_with(id=999)
    mock_filter.return_value.first.assert_awaited_once()
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Documento não encontrado."
