import openai
from typing import Dict, Any, List, Optional
from app.core.config import settings

class OpenRouterClient:
    """OpenRouter API客户端封装"""
    
    def __init__(self):
        # Configure OpenAI client to use OpenRouter
        openai.api_key = settings.OPENROUTER_API_KEY
        openai.api_base = settings.OPENROUTER_BASE_URL
        
        self.model = settings.OPENROUTER_MODEL
        self.headers = {
            "HTTP-Referer": "http://localhost:8000",  # Required by OpenRouter
            "X-Title": "Chinese LLM Knowledge Base"    # Application identifier
        }
    
    def chat_completion(self, 
                        messages: List[Dict[str, str]], 
                        temperature: float = 0.3,
                        max_tokens: Optional[int] = None) -> Dict[str, Any]:
        """发送聊天请求到OpenRouter"""
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                headers=self.headers
            )
            return response
        except openai.error.RateLimitError as e:
            print(f"OpenRouter速率限制: {e}")
            # Wait and retry or return error
            import time
            time.sleep(5)
            return {"error": "速率限制，请稍后再试"}
        except Exception as e:
            print(f"OpenRouter请求错误: {e}")
            return {"error": str(e)}
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """获取可用模型列表"""
        try:
            response = openai.Model.list()
            return response.get("data", [])
        except Exception as e:
            print(f"获取模型列表错误: {e}")
            return []
