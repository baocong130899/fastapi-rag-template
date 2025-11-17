from fastapi import APIRouter, UploadFile, Depends
from dependency_injector.wiring import inject, Provide
from app.presentation.api.dependencies import get_current_user
from app.presentation.schemas.user_schemas import UserResponse
from app.application.validation import DocumentUploadValidator
from app.bootstrap.container import Container

router = APIRouter()


@router.post("/upload")
@inject
async def upload(
    file: UploadFile,
    current_user: UserResponse = Depends(get_current_user),
    document_upload_validator: DocumentUploadValidator = Depends(Provide[Container.document_upload_validator])
):
    await document_upload_validator.validate(file=file)
    print(current_user, flush=True)
