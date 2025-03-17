from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    DocumentIngestionRequest, 
    DocumentIngestionResponse,
    QueryRequest,
    QueryResponse
)
from app.services.knowledge_base import KnowledgeBaseService

router = APIRouter()

@router.post("/ingest", response_model=DocumentIngestionResponse)
async def ingest_documents(request: DocumentIngestionRequest):
    """Import documents to knowledge base"""
    kb_service = KnowledgeBaseService(collection_name="default_collection")
    result = kb_service.ingest_documents(directory_path=request.directory_path)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    
    return result

@router.post("/query", response_model=QueryResponse)
async def query_knowledge_base(request: QueryRequest):
    """Query knowledge base"""
    kb_service = KnowledgeBaseService(collection_name=request.collection_name)
    result = kb_service.query_knowledge_base(request.query)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result

@router.post("/query_with_model", response_model=QueryResponse)
async def query_knowledge_base_with_model(request: QueryRequestWithModel):
    """Query knowledge base using specified model"""
    # Temporarily set environment variables
    import os
    original_provider = os.environ.get("LLM_PROVIDER")
    original_model = os.environ.get("OPENROUTER_MODEL")
    
    try:
        os.environ["LLM_PROVIDER"] = "openrouter"
        os.environ["OPENROUTER_MODEL"] = request.model
        
        kb_service = KnowledgeBaseService(collection_name=request.collection_name)
        result = kb_service.query_knowledge_base(request.query)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
    finally:
        # Restore original settings
        if original_provider:
            os.environ["LLM_PROVIDER"] = original_provider
        if original_model:
            os.environ["OPENROUTER_MODEL"] = original_model
