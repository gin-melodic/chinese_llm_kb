import os
from typing import Dict, Any, List
from app.services.document_processor import DocumentProcessor
from app.services.vector_store import VectorStoreService
from app.services.llm_service import LLMService

class KnowledgeBaseService:
    """知识库管理服务，整合文档处理和查询功能"""
    
    def __init__(self, collection_name: str = "default_collection"):
        self.collection_name = collection_name
        self.document_processor = DocumentProcessor()
        self.vector_store_service = VectorStoreService(collection_name=collection_name)
        self.llm_service = None  # Lazy initialization
    
    def ingest_documents(self, directory_path: str) -> Dict[str, Any]:
        """处理并导入文档到知识库"""
        try:
            # Validate directory
            if not os.path.exists(directory_path):
                return {"success": False, "message": f"directory {directory_path} does not exist"}
            
            # Load documents
            documents = self.document_processor.load_documents(directory_path)
            if not documents:
                return {"success": False, "message": "No documents found in specified directory"}
            
            # Split documents
            splits = self.document_processor.split_documents(documents)
            
            # Create vector store
            self.vector_store_service.create_from_documents(splits)
            
            return {
                "success": True, 
                "message": f"Successfully imported {len(documents)} documents, created {len(splits)} document chunks"
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def query_knowledge_base(self, query: str) -> Dict[str, Any]:
        """查询知识库"""
        # Lazy initialization of LLM service
        if self.llm_service is None:
            self.llm_service = LLMService(collection_name=self.collection_name)
        
        return self.llm_service.query(query)
