from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.config import settings
from app.core.database import init_vector_extension
from fastapi.middleware.wsgi import WSGIMiddleware
from app.gradio_ui import create_gradio_interface
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Execute on startup
    init_vector_extension()
    # Mount gradio service
    import threading
    threading.Thread(target=gradio_app.launch, 
                    kwargs={"server_port": settings.GRADIO_PORT}).start()
    yield
    # Execute on shutdown
    pass

app = FastAPI(
    title=settings.APP_NAME,
    description="基于OpenAI API的中文私有知识库",
    version="1.0.0",
    lifespan=lifespan
)

# Mount Gradio in FastAPI
gradio_app = create_gradio_interface()
app.mount("/gradio", WSGIMiddleware(gradio_app.server))

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "欢迎使用中文私有LLM知识库API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host=settings.API_HOST, 
        port=settings.API_PORT,
        reload=True
    )
