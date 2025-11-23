from fastapi import APIRouter, Request
from app.presentation.api.v1.endpoints import (
    auth_router,
    user_router,
    knowledge_base_router,
    document_router,
)

api_router = APIRouter()

@api_router.get("")
async def root(request: Request):
    # show some useful info for debugging
    client_host = request.client.host if request.client else None
    scheme = request.url.scheme
    host = request.headers.get("host")
    xff = request.headers.get("x-forwarded-for")
    proto = request.headers.get("x-forwarded-proto")
    return {
        "msg": "hello from fastapi",
        "request_client_host": client_host,
        "request_url_scheme": scheme,
        "host_header": host,
        "x_forwarded_for": xff,
        "x_forwarded_proto": proto,
    }

@api_router.get("/health", tags=["Health check"])
def health():
    return {
        "status": True
    }

api_router.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
api_router.include_router(user_router.router, prefix="/users", tags=["User"])
api_router.include_router(knowledge_base_router.router, prefix="/knowledge-base", tags=["Knowledge base"])
api_router.include_router(document_router.router, prefix="/documents", tags=["Document"])