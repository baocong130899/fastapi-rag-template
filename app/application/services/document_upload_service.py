from typing import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.messaging import BaseMessagingClient
from app.domain.respositories import DocumentRepository


class DocumentUploadService:
    def __init__(
        self, 
        messaging_client: BaseMessagingClient,
        document_repo: DocumentRepository,
        session_factory: AsyncIterator[AsyncSession],
    ):
        self.messaging_client = messaging_client
        self.document_repo = document_repo
        self.session_factory = session_factory


    async def upload_document(
        self,
        user_id: str,
        file_path: str,
        file_name: str, 
        file_size: int,
        content_type: str,
        hexdigest: str,
    ):
        """
        """
        try:
            # Check document exists.
            # Create domain document entity.
            # Send to rabbbitmq for processing.
            # Update status.

            pass
        except Exception as e:
            raise Exception(f"Failed to upload document: {str(e)}")