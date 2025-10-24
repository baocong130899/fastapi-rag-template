from fastapi import APIRouter
from app.presentation.api.v1.endpoints import auth_router
from app.presentation.api.v1.endpoints import user_router

api_router = APIRouter()

@api_router.get("/health", tags=["Health check"])
def health():
    return {
        "status": True
    }

api_router.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
api_router.include_router(user_router.router, prefix="/users", tags=["User"])
