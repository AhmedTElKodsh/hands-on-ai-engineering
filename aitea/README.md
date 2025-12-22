# AITEA Application

> **📍 CURRENT STATUS: Phase 3 - Multi-Provider LLM System**
>
> This package implements the AITEA (AI Time Estimation Agent) application with multi-provider LLM fallback support.
> The application automatically detects available API keys and falls back through providers in priority order.
>
> **Implemented**: Multi-provider detection, environment configuration, MockLLM fallback
> **Next Phase**: CLI interface (Phase 2, Task 12) and FastAPI web application (Phase 10, Task 64)

AI Time Estimation Agent - A project-based learning curriculum for building production-ready AI agents.

## Quick Start

### 1. Install Dependencies

```bash
# Activate conda environment
conda activate aitea

# Install web dependencies
uv pip install fastapi uvicorn python-dotenv websockets sse-starlette
```

**Note**: The `python-dotenv` package is now imported in `app.py` to support environment variable loading from `.env` files.

### 2. Configure Environment

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
# Edit .env with your actual API keys
```

### 3. Run the Application

```bash
# Development mode with auto-reload
python app.py

# Or using uvicorn directly
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access the API

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### REST Endpoints

#### Health Check

```bash
GET /health
```

#### Estimate Project

```bash
POST /api/estimate
Content-Type: application/json

{
  "features": ["CRUD", "Authentication", "Dashboard"],
  "use_rag": false
}
```

#### List Features

```bash
GET /api/features?team=backend
```

### Streaming Endpoints

#### Server-Sent Events (SSE)

```bash
GET /api/estimate/stream?features=CRUD,Auth,Dashboard
```

Example client:

```javascript
const eventSource = new EventSource("/api/estimate/stream?features=CRUD,Auth");
eventSource.onmessage = (event) => {
  console.log("Progress:", JSON.parse(event.data));
};
```

### WebSocket Endpoints

#### Agent Communication

```bash
WS /ws/agent
```

Example client:

```javascript
const ws = new WebSocket("ws://localhost:8000/ws/agent");
ws.onopen = () => {
  ws.send(JSON.stringify({ message: "Estimate project X" }));
};
ws.onmessage = (event) => {
  console.log("Response:", JSON.parse(event.data));
};
```

## Testing the API

### Using curl

```bash
# Health check
curl http://localhost:8000/health

# Estimate project
curl -X POST http://localhost:8000/api/estimate \
  -H "Content-Type: application/json" \
  -d '{"features": ["CRUD", "Auth"], "use_rag": false}'

# Stream estimation
curl -N http://localhost:8000/api/estimate/stream?features=CRUD,Auth
```

### Using Python

```python
import requests

# Health check
response = requests.get("http://localhost:8000/health")
print(response.json())

# Estimate project
response = requests.post(
    "http://localhost:8000/api/estimate",
    json={"features": ["CRUD", "Auth"], "use_rag": False}
)
print(response.json())
```

## Project Structure

```
aitea/
├── app.py              # Main FastAPI application (imports dotenv for env loading)
├── .env                # Environment variables (not in git)
├── .env.example        # Example environment file
├── .gitignore          # Git ignore patterns
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── PACKAGE_INFO.md    # Package configuration details
```

## Current Implementation Status

The `app.py` file currently includes:

- ✅ Basic imports: `os`, `pathlib.Path`
- ✅ Environment variable support: `dotenv.load_dotenv`
- ⏳ FastAPI application setup (pending Phase 10, Task 64.1)
- ⏳ REST endpoints (pending Phase 10, Task 64.1)
- ⏳ WebSocket support (pending Phase 10, Task 64.2)
- ⏳ SSE streaming (pending Phase 10, Task 64.3)

## Development

### Adding New Endpoints

1. Define request/response models using Pydantic
2. Add endpoint function with appropriate decorator
3. Implement business logic (integrate with aitea-core services)
4. Add tests in `tests/` directory

### Integrating with aitea-core

```python
# app.py - Current implementation
import os
import pathlib as Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
openai_key = os.getenv("OPENAI_API_KEY")
data_dir = os.getenv("AITEA_DATA_DIR", "./data")

# Future implementation (Phase 10, Task 64.1):
# from src.services.interfaces import IEstimationService
# from src.services.estimation import EstimationService
#
# # Initialize service
# estimation_service = EstimationService()
#
# # Use in endpoint
# @app.post("/api/estimate")
# async def estimate_project(request: EstimateRequest):
#     result = estimation_service.estimate_project(request.features)
#     if result.is_err():
#         raise HTTPException(status_code=400, detail=str(result.unwrap_err()))
#     return result.unwrap()
```

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Configuration

```bash
# Use production ASGI server
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process or use a different port
uvicorn app:app --port 8001
```

### Import Errors

```bash
# Ensure aitea-core is installed
cd ..
uv pip install -e .
```

### CORS Issues

Update CORS configuration in `app.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Implementation Roadmap

This web application will be built progressively through the AITEA curriculum:

### Phase 10: Deployment & Integration (Tasks 64-68)

**Task 64: FastAPI Web Application**

- [ ] 64.1 Create FastAPI app with REST endpoints
- [ ] 64.2 Add WebSocket endpoint for bidirectional agent communication
- [ ] 64.3 Implement SSE endpoint for streaming updates
- [ ] 64.4 Add Pydantic response models and error handling
- [ ] 64.5 Write property test for API endpoint response consistency
- [ ] 64.6 Write property test for WebSocket message ordering

**Task 65: Queue-Based Processing**

- [ ] 65.1 Set up Redis for task queue
- [ ] 65.2 Implement Celery workers for long-running agent tasks
- [ ] 65.3 Add task status tracking and result retrieval
- [ ] 65.4 Implement task prioritization and rate limiting

**Task 66: Containerization**

- [ ] 66.1 Create Dockerfile for AITEA application
- [ ] 66.2 Create docker-compose for local development
- [ ] 66.3 Add health checks and graceful shutdown
- [ ] 66.4 Document Kubernetes deployment patterns

**Task 67: Serverless Deployment**

- [ ] 67.1 Create AWS Lambda handler for estimation API
- [ ] 67.2 Implement Vercel serverless functions
- [ ] 67.3 Add cold start optimization strategies
- [ ] 67.4 Document serverless limitations and workarounds

### Prerequisites

Before implementing this web application, complete:

1. **Phase 1-2**: Core models, services, and CLI (aitea-core)
2. **Phase 3**: LLM fundamentals and multi-provider fallback
3. **Phase 4**: Document processing and chunking (aitea-ingest)
4. **Phase 5-6**: Agent foundations and LangChain integration
5. **Phase 7-8**: Multi-agent frameworks and advanced RAG
6. **Phase 9**: Production hardening (guardrails, observability, reliability)

### Current Implementation Status

- ✅ **aitea-core**: Models, services, utilities (Phases 1-2)
- ✅ **aitea-cli**: Typer CLI with Rich UI (Phase 2)
- ✅ **LLM Fundamentals**: MockLLM, multi-provider fallback (Phase 3)
- ✅ **Document Processing**: Loaders, chunking strategies (Phase 4)
- ✅ **Agent Foundations**: SimpleAgent, ToolRegistry, ReAct, Memory (Phase 5)
- ✅ **LangChain Integration**: LCEL chains, custom tools, vector stores (Phase 6)
- ✅ **Multi-Agent Frameworks**: CrewAI, AutoGen implementations (Phase 7)
- ⏳ **LlamaIndex & Advanced RAG**: In progress (Phase 8)
- ⏳ **Production Hardening**: Not started (Phase 9)
- ⏳ **Web Application**: Not started (Phase 10) ← **YOU ARE HERE**

## Next Steps

1. Complete Phase 9 (Production Hardening) first:

   - Implement guardrails (NeMo, Guardrails AI)
   - Add observability (LangFuse, Phoenix, OpenTelemetry)
   - Implement reliability patterns (retries, circuit breakers, fallbacks)
   - Add async patterns and streaming support

2. Then begin Phase 10 (Web Application):
   - Start with Task 64.1: Create basic FastAPI app
   - Integrate with existing aitea-core services
   - Add WebSocket and SSE endpoints
   - Implement queue-based processing
   - Containerize and deploy

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [WebSocket Guide](https://fastapi.tiangolo.com/advanced/websockets/)
- [SSE with FastAPI](https://github.com/sysid/sse-starlette)
- [AITEA Curriculum](../curriculum/README.md)
