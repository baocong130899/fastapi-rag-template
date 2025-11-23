from app.infrastructure.messaging import BaseMessagingClient


class DocumentUploadService:
    def __init__(
        self, 
        messaging_client: BaseMessagingClient
    ):
        self.messaging_client = messaging_client

    async def upload_document(self):
        """
        """
        try:
            pass    
        except Exception as e:
            raise Exception(f"Failed to upload document: {str(e)}")