from fastapi import APIRouter
from app.api.endpoints import knowledge_base

api_router = APIRouter()
api_router.include_router(knowledge_base.router, prefix="/knowledge_base", tags=["知识库"])
