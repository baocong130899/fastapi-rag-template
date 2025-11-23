from fastapi import APIRouter, UploadFile, Depends
from dependency_injector.wiring import inject, Provide
from app.presentation.api.dependencies import get_current_user
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
    document_upload_validator: DocumentUploadValidator = Depends(Provide[Container.document_upload_validator]),
    temp_file_helper: TempFileHelper = Depends(Provide[Container.temp_file_helper])
):
    await document_upload_validator.validate(file=file)
    data_file = await temp_file_helper.save_temp(file=file)
    print(data_file, flush=True)
    
