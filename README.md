# Chinese LLM Knowledge Base

A Chinese knowledge base system based on Large Language Models, supporting document import, knowledge retrieval, and intelligent Q&A.

## Features

- 📚 Multi-format Document Support: PDF, Word, Excel, and other common document formats
- 🔍 Intelligent Retrieval: Efficient semantic search based on vector database
- 💬 Smart Q&A: Natural language interaction powered by LLM
- 🎯 Precise Matching: Hybrid search combining keywords and semantics
- 🎨 User-friendly Interface: Gradio-based interactive UI
- 🚀 Containerized Deployment: Quick deployment with Docker

## Tech Stack

- Backend Framework: FastAPI
- AI Models: LangChain + OpenAI
- Vector Database: PostgreSQL + pgvector
- Document Processing: unstructured, PyMuPDF, python-docx, openpyxl
- Frontend Interface: Gradio
- Deployment: Docker + Docker Compose

## Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL 13+
- Docker (optional)

### Installation

1. Clone the repository
```bash
git clone [repository-url]
cd chinese_llm_kb
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
```bash
cp .env.example .env
# Edit .env file with your configuration:
# - Set your OpenRouter API key (required)
# - Configure database credentials
# - Adjust other settings as needed
```

### Environment Variables

The following environment variables need to be configured in your `.env` file:

#### Required Variables
- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `DB_PASSWORD`: Your PostgreSQL database password
- `DB_NAME`: Database name (default: vector_db)

#### Optional Variables
- `OPENAI_API_KEY`: Your OpenAI API key (if using OpenAI models)
- `DB_HOST`: Database host (default: localhost)
- `DB_PORT`: Database port (default: 5432)
- `DB_USER`: Database user (default: postgres)
- `API_HOST`: API host (default: 127.0.0.1)
- `API_PORT`: API port (default: 8000)
- `GRADIO_PORT`: Gradio UI port (default: 7860)
- `EMBEDDING_MODEL`: Embedding model name (default: moka-ai/m3e-base)

### Docker Deployment

```bash
docker-compose up -d
```

## Project Structure

```
.
├── app/                    # Main application directory
│   ├── api/               # API endpoints
│   ├── core/              # Core functionality
│   ├── models/            # Data models
│   ├── services/          # Business services
│   └── utils/             # Utility functions
├── data/                  # Data directory
├── tests/                 # Test cases
├── docker-compose.yml     # Docker compose configuration
├── Dockerfile            # Docker build file
└── requirements.txt      # Project dependencies
```

## Usage Guide

1. Start the service
```bash
python run.py
```

2. Access interfaces
- Web Interface: http://localhost:7860
- API Documentation: http://localhost:8000/docs

## Development Guide

### Adding New Features

1. Add business logic in `app/services`
2. Add API endpoints in `app/api`
3. Define data models in `app/models`
4. Add test cases in `tests`

### Code Standards

- Follow PEP 8 coding style
- Use type annotations
- Write detailed docstrings

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests to help improve the project.