import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

# Test connection
def test_openrouter():
    try:
        response = openai.ChatCompletion.create(
            model="qwen/qwq-32b:free",
            messages=[
                {"role": "user", "content": "你好，介绍一下Gemini 2.0模型的特点"}
            ],
            headers={
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "Chinese LLM Knowledge Base Test"
            }
        )
        print("成功连接OpenRouter!")
        print(f"模型回复: {response.choices[0].message.content}")
    except Exception as e:
        print(f"连接失败: {e}")

if __name__ == "__main__":
    test_openrouter()
