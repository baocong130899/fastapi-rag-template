from fastapi import APIRouter, UploadFile, Depends
from dependency_injector.wiring import inject, Provide
from app.presentation.api.dependencies import get_current_user
from app.application.services import DocumentUploadService
from app.presentation.schemas.user_schemas import UserResponse
from app.application.validation import DocumentUploadValidator
from app.infrastructure.helpers import TempFileHelper
from app.bootstrap.container import Container

router = APIRouter()


@router.post("/upload")
@inject
async def upload(
    file: UploadFile,
    current_user: UserResponse = Depends(get_current_user),
    document_upload_service: DocumentUploadService = Depends(Provide[Container.document_upload_service]),
    document_upload_validator: DocumentUploadValidator = Depends(Provide[Container.document_upload_validator]),
    temp_file_helper: TempFileHelper = Depends(Provide[Container.temp_file_helper])
):
    await document_upload_validator.validate(file=file)
    data_file = await temp_file_helper.save_temp(file=file)

    await document_upload_service.upload_document(
        user_id=current_user.id,
        file_path=data_file.dest_path,
        file_name=data_file.file_name,
        file_size=data_file.file_size,
        content_type=data_file.content_type,
        hexdigest=data_file.hexdigest,
    )
    
