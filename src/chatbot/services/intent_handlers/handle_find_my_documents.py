from src.documents.service import get_my_documents

class FindMyDocumentsHandler:
    async def handle(self, user_id: str) -> str:
        documents = await get_my_documents(user_id)
        
        if not documents:
            return "Você não possui documentos cadastrados."

        resposta = "Seus documentos cadastrados são:\n"
        for doc in documents:
            resposta += f"- {doc.document_type}: {doc.document_number}\n"
        
        return resposta.strip()

find_my_documents_handler = FindMyDocumentsHandler()
