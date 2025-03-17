from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class DocumentIngestionRequest(BaseModel):
    directory_path: str = Field(..., description="包含要导入文档的目录路径")

class DocumentIngestionResponse(BaseModel):
    success: bool
    message: str

class QueryRequest(BaseModel):
    query: str = Field(..., description="要在知识库中搜索的查询字符串")
    collection_name: str = Field(default="default_collection", description="要搜索的集合名称")

class SourceDocument(BaseModel):
    content: str
    metadata: Dict[str, Any]

class QueryResponse(BaseModel):
    answer: Optional[str] = None
    source_documents: Optional[List[SourceDocument]] = None
    error: Optional[str] = None

class QueryRequestWithModel(BaseModel):
    query: str = Field(..., description="要在知识库中搜索的查询字符串")
    collection_name: str = Field(default="default_collection", description="要搜索的集合名称")
    model: str = Field(default="google/gemini-2.0-flash-exp:free", description="要使用的模型")
