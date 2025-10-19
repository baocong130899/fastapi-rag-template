# 🚀 FastAPI-RAG-Template – Retrieval-Augmented Generation with LangChain & PGVector

<div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
  <a href="https://github.com/baocong130899/fastapi-rag-template/stargazers" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/github/stars/baocong130899/fastapi-rag-template" alt="GitHub stars">
  </a>

  <a href="https://github.com/baocong130899/fastapi-rag-template/issues" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/github/issues/baocong130899/fastapi-rag-template" alt="GitHub issues">
  </a>

  <a href="LICENSE" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/github/license/baocong130899/fastapi-rag-template" alt="License">
  </a>

  <a href="https://www.docker.com/" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/docker-ready-blue" alt="Docker">
  </a>

  <a href="https://fastapi.tiangolo.com/" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/FastAPI-Framework-brightgreen" alt="FastAPI">
  </a>

  <a href="https://alembic.sqlalchemy.org/en/latest/" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/Alembic-Framework-orange" alt="Alembic">
  </a>

  <a href="https://docs.langchain.com/" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/LangChain-Enabled-orange" alt="LangChain">
  </a>
</div>

> **A production-ready template for building Retrieval-Augmented Generation (RAG) systems** with **FastAPI**, **LangChain**, and **PostgreSQL + PGVector**.  
> Build scalable LLM-powered applications with vector search, modular pipelines and ready-to-deploy infrastructure.

---

## 📌 Table of Contents  
- [🚀 Project Overview](#🚀-project-overview)  
- [🌟 Features](#🌟-features)  
- [🏗️ Tech Stack](#🏗️-tech-stack)  
- [🧭 Demo](#🧭-demo)  
- [⚙️ Installation & Setup](#⚙️-installation--setup)  
- [📁 Project Structure](#📁-project-structure)  
- [📡 API Endpoints](#📡-api-endpoints)   
- [🧩 Integration](#🧩-integration)  
- [📈 Roadmap](#📈-roadmap)  
- [🛠️ Contributing](#🛠️-contributing)  
- [🐞 Known Issues](#🐞-known-issues)  
- [🏷️ Topics](#🏷️-topics)  
- [📄 License](#🪪-license)  
- [💫 Author](#💫-author)  
- [📝 Last Updated](#📝-last-updated)  

---

## 🚀 Project Overview  
This template solves the common challenge of building **RAG-powered backends** by providing a **clean architecture** that combines vector retrieval and LLM generation. With this template, you get:  
- Embedding documents into PGVector  
- Searching vectors to get relevant context  
- Generating responses via LangChain + LLM  
- Serving everything via FastAPI asynchronously  
- Dockerized services + Nginx reverse proxy for production readiness

Use case examples: chatbots, Q&A systems over custom documents, knowledge-base assistants, internal tools.

---

## 🌟 Features  
- 🔍 **Retrieval-Augmented Generation (RAG)** architecture  
- 🧩 Modular pipelines: embedding → retrieval → generation  
- 🗃️ **PGVector + PostgreSQL** for vector storage & search  
- ⚡ **FastAPI** async backend for high performance  
- 🐳 **Dockerized**: ready for local & production deployment  
- 🧱 Domain-Driven Design (DDD) for maintainability  
- 📊 Optional integration: Langfuse / LangWatch / Prometheus  
- 🌐 Nginx reverse proxy setup included (CORS, HTTPS-ready)  

---

## 🏗️ Tech Stack  
| Layer            | Technology                         |
|------------------|-----------------------------------|
| Backend API      | FastAPI                           |
| LLM Framework    | LangChain                          |
| Migration        | Alembic                           |
| Vector Database  | PGVector / PostgreSQL              |
| Containerization | Docker + Docker Compose            |
| Reverse Proxy    | Nginx                              |
| Scheduler        | APScheduler (async)                |
| Monitoring       | Langfuse / LangWatch / Prometheus  |

---

## 🧭 Demo  
> _Insert a GIF or screenshot of the API in use_  
![Demo](./assets/demo.gif)

---

## ⚙️ Installation & Setup
### 1️⃣ Clone the repository

```bash
git clone https://github.com/baocong130899/fastapi-rag-template.git

cd fastapi-rag-template  
```

### 2️⃣ Setup environment
You can check the details in the configuration table below.

```bash
cp .env.example .env 
```

### 3️⃣ Build & run with Docker

```bash
docker compose up -d --build  
```

### 4️⃣ Verification
Access the following URLs after service startup:

📚 API Documentation: [http://127.0.0.1/redoc](http://127.0.0.1/redoc)

---

## 📁 Project Structure
### 📁 Structure
```
fastapi-rag-template/
├── app/                                 # Main application source code
│   ├── application/                     # Application layer: use cases & orchestration logic
│   │   ├── services/                    # Application Services / UseCases
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── user_service.py
│   │   └── __init__.py
│   │
│   ├── bootstrap/                       # Application bootstrap / dependency container
│   │   ├── container.py
│   │   ├── __init__.py
│   │
│   ├── config/                          # Global configuration (env vars, settings, logging, etc.)
│   │   ├── settings.py
│   │   ├── logging_config.py
│   │   └── __init__.py
│   │
│   ├── domain/                          # Domain core: business logic & rules
│   │   ├── entities/                    # Domain Entities
│   │   ├── value_objects/               # Domain Value Objects
│   │   ├── aggregates/                  # Aggregate Roots (optional)
│   │   ├── repositories/                # Abstract repository interfaces
│   │   ├── events/                      # Domain events (if using event-driven patterns)
│   │   └── __init__.py
│   │
│   ├── infrastructure/                  # Technical infrastructure layer
│   │   ├── enums/                       # Enum definitions (status, roles, etc.)
│   │   ├── models/                      # ORM models (SQLAlchemy)
│   │   ├── repository_impl/             # Repository implementations for domain interfaces
│   │   ├── external/                    # External service or API integrations
│   │   ├── database.py                  # Database connection, ORM setup, Alembic migrations
│   │   └── __init__.py
│   │
│   ├── presentation/                    # Presentation layer (API / HTTP interfaces)
│   │   ├── api/                         # Routers & Controllers
│   │   │   ├── v1/                      # API versioning (v1, v2, etc.)
│   │   │   │   ├── endpoints/           # Route handler files
│   │   │   │   └── dependencies.py      # Dependency injection for routers
│   │   │   └── __init__.py
│   │   ├── schemas/                     # Pydantic schemas (Request/Response models)
│   │   └── __init__.py
│   │
│   ├── utils/                           # Utility helpers & common functions
│   │   └── __init__.py
│   │
│   └── rag/                             # RAG (Retrieval-Augmented Generation) module
│   │   ├── __init__.py
│   │   ├── adapters/                    # Integration adapters for external LLM/Vector APIs
│   │   │   ├── __init__.py
│   │   │   ├── langchain_adapter.py
│   │   │   ├── openai_adapter.py
│   │   │   └── vectorstore_adapter.py   # PGVector / Chroma / FAISS implementation
│   │   │
│   │   ├── pipelines/                   # RAG pipelines (embedding, retrieval, generation)
│   │   │   ├── __init__.py
│   │   │   ├── embedding_pipeline.py    # Embedding + storing documents
│   │   │   ├── retrieval_pipeline.py    # Vector similarity search logic
│   │   │   └── generation_pipeline.py   # LLM response generation & synthesis
│   │   │
│   │   ├── services/                    # Service orchestrators for RAG flow
│   │   │   ├── __init__.py
│   │   │   └── rag_service.py           # Main RAG Orchestrator Service
│   │   │
│   │   └── schemas/                     # Request/Response schemas for RAG API
│   │       ├── __init__.py
│   │       └── rag_schema.py
│   │ 
│   ├── main.py                          # Entry point: initializes FastAPI app, loads configs, includes routers
│   │ 
├── migration/                           # Alembic database migrations
│   ├── versions/
│   │   ├── <timestamp>_init_db.py       # Initial migration script
│   ├── env.py                           # Alembic environment setup
│   ├── script.py.mako                   # Migration script template
│   └── README                           # Notes about migrations
│    
└── tests/                               # Unit & integration tests
    ├── domain/
    ├── application/
    └── presentation/
```
### 🔁 Flow
Request:

```
Request 
    → Presentation (API)
    → Application (Use Case)
    → Domain (Business Logic)
    → Infrastructure (Persistence / External)
```

Response:
```
Infrastructure → Domain → Application → Presentation → Response
```

## 📡 API Endpoints

| Endpoint         | Method | Description                           |
| ---------------- | ------ | ------------------------------------- |
| `/api/v1/embed`  | POST   | Upload and embed documents            |
| `/api/v1/query`  | POST   | Query retrieval + generation workflow |
| `/api/v1/health` | GET    | Health check endpoint                 |

---

## 🧩 Integration

You can optionally integrate observability tools like Langfuse.
Wrap your pipelines to track LLM latency, cost, and usage easily.

---

## 📈 Roadmap

* [ ] Add Hybrid Search (BM25 + Vector)
* [ ] Add Authentication (JWT + OAuth)
* [ ] Integrate Langfuse tracing
* [ ] Build nextjs frontend demo
* [ ] Increase test coverage

---

## 🛠️ Contributing

We welcome contributions! Please review the following steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes with clear messages
4. Push to your fork and open a Pull Request
5. Ensure all CI checks pass and include documentation / test where needed

Read [CLICENSE](CLICENSE) for more details.

---

## 🐞 Known Issues

* 🤖 LLM prompt drift may occur with large contexts — consider context chunking
* ⚠️ PGVector search latency increases for very large datasets (~100M vectors)
* 🚧 Deployment scripts assume Linux environment — Mac/Windows users may need adjustments

---

## 🏷️ Topics

`rag`, `fastapi`, `langchain`, `pgvector`, `llm`,  
`retrieval-augmented-generation`, `vector-database`,  
`docker`, `nginx`, `openai`, `ai-backend`,
`langfuse`, `langwatch`, `python`, `chatbot`, `template`

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

---

## 💫 Author

**Lê Công**  
GitHub: [@baocong130899](https://github.com/baocong130899)  
Email: [lebaocongct@gmail.com](mailto:lebaocongct@gmail.com)

---

## 📝 Last Updated

*Last updated: 2025-10-18*