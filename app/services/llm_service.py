from typing import Dict, Any, List
import openai
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from app.core.config import settings
from app.services.vector_store import VectorStoreService

class LLMService:
    """LLM service, based on OpenAI API for question answering"""
    
    def __init__(self, collection_name: str = "default_collection"):
        self.vector_store_service = VectorStoreService(collection_name=collection_name)
        self.llm = self._initialize_llm()
        self.qa_chain = self._initialize_qa_chain()
    
    def _initialize_llm(self):
        """Initialize LLM model, supports multiple providers"""
        if settings.LLM_PROVIDER == "openrouter":
            # Use OpenRouter's Gemini 2.0 Flash model
            return ChatOpenAI(
                model=settings.OPENROUTER_MODEL,
                openai_api_key=settings.OPENROUTER_API_KEY,
                openai_api_base=settings.OPENROUTER_BASE_URL,
                temperature=0.3,
                max_retries=2,  # Number of retries
                request_timeout=60,  # Request timeout in seconds
                headers={
                    "HTTP-Referer": "http://localhost:8000",  # Required by OpenRouter
                    "X-Title": "Chinese LLM Knowledge Base"    # Application name
                }
            )
        # elif settings.LLM_PROVIDER == "openai":
        #     # Use OpenAI
        #     return ChatOpenAI(
        #         api_key=settings.OPENAI_API_KEY,
        #         model_name="gpt-3.5-turbo",
        #         temperature=0.3
        #     )
    
    def _initialize_qa_chain(self):
        """Initialize question answering chain"""
        retriever = self.vector_store_service.get_retriever()
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )
    
    def query(self, question: str) -> Dict[str, Any]:
        """Query knowledge base"""
        try:
            # System prompt for Chinese
            system_prompt = """You are a professional Chinese knowledge assistant based on the provided context to answer user questions.
            If there is no relevant information in the context, please directly state that you don't know.
            The answer should be complete, clear, and professional."""
            
            # Handle potential rate limits
            try:
                result = self.qa_chain({"query": question})
            except openai.error.RateLimitError:
                # Fallback for rate limits
                print("OpenRouter rate limit, retrying...")
                import time
                time.sleep(2)  # Wait 2 seconds before retry
                result = self.qa_chain({"query": question})
            
            # Extract source document information
            source_documents = []
            if "source_documents" in result:
                for doc in result["source_documents"]:
                    source_documents.append({
                        "content": doc.page_content,
                        "metadata": doc.metadata
                    })
            
            return {
                "answer": result["result"],
                "source_documents": source_documents
            }
        except Exception as e:
            print(f"Error querying LLM: {e}")
            return {"error": str(e)}