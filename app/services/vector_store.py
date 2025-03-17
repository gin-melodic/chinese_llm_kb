from typing import List, Any, Optional
from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from langchain.vectorstores import PGVector
from app.core.config import settings

class VectorStoreService:
    """向量存储服务，负责文档嵌入和检索"""
    
    def __init__(self, collection_name: str = "default_collection"):
        self.collection_name = collection_name
        self.connection_string = settings.DATABASE_URL
        self.embeddings = self._initialize_embeddings()
    
    def _initialize_embeddings(self):
        """初始化嵌入模型，优先使用针对中文优化的模型"""
        if settings.EMBEDDING_MODEL and "m3e" in settings.EMBEDDING_MODEL:
            # Use embedding model optimized for Chinese
            return HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL,
                model_kwargs={'device': 'cpu'}
            )
        else:
            # If not specified, use OpenAI's embedding model
            return OpenAIEmbeddings(
                api_key=settings.OPENAI_API_KEY
            )
    
    def create_from_documents(self, documents: List[Any]) -> None:
        """从文档创建向量存储"""
        try:
            PGVector.from_documents(
                documents=documents,
                embedding=self.embeddings,
                collection_name=self.collection_name,
                connection_string=self.connection_string
            )
            print(f"成功创建向量存储，包含 {len(documents)} 个文档块")
        except Exception as e:
            print(f"创建向量存储时出错: {e}")
            raise
    
    def get_retriever(self, search_type: str = "mmr", k: int = 4):
        """获取向量检索器"""
        try:
            vector_store = PGVector(
                collection_name=self.collection_name,
                connection_string=self.connection_string,
                embedding_function=self.embeddings
            )
            
            return vector_store.as_retriever(
                search_type=search_type,
                search_kwargs={"k": k}
            )
        except Exception as e:
            print(f"获取检索器时出错: {e}")
            raise
