# 🚀 FastAPI-RAG-Template – Retrieval-Augmented Generation with LangChain & PGVector

<div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
  <a href="https://github.com/baocong130899/rag/stargazers" target="_blank" rel="noopener noreferrer">
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
docker-compose up -d --build  
```

### 4️⃣ Verification
Access the following URLs after service startup:

📚 API Documentation: [http://127.0.0.1/redoc](http://127.0.0.1/redoc)

---

## 📁 Project Structure
### Structure
```
fastapi-rag-template/
├── app/                    # mã nguồn chính
│   ├── main.py             # entry point, khởi tạo FastAPI app, load config, include routers
│   ├── config/             # cấu hình tổng (settings, env, logger, etc.)
│   │   ├── settings.py
│   │   └── __init__.py
│   ├── presentation/       # layer tương tác bên ngoài: API endpoints, HTTP layer
│   │   ├── api/             # các router / controller
│   │   │   ├── v1/           # nếu versioning API
│   │   │   │   ├── endpoints/  # các route files
│   │   │   │   └── dependencies/
│   │   │   └── __init__.py
│   │   ├── schemas/         # Pydantic models request/response
│   │   └── __init__.py
│   ├── application/         # layer ứng dụng / use cases / services
│   │   ├── services/         # các UseCase / Application Service
│   │   ├── dtos/             # optional: các DTO nếu cần chuyển giữa layers
│   │   └── __init__.py
│   ├── domain/              # domain core: nghiệp vụ
│   │   ├── entities/         # các Entity
│   │   ├── value_objects/
│   │   ├── aggregates/       # nếu mô hình hóa aggregates
│   │   ├── repositories/     # định nghĩa interface (abstract) của repository
│   │   ├── domain_services/  # nghiệp vụ không rõ nên thuộc entity nào
│   │   ├── events/           # domain events
│   │   └── __init__.py
│   ├── infrastructure/      # lớp bên ngoài hỗ trợ kỹ thuật
│   │   ├── database/         # kết nối DB, ORM, migrations
│   │   ├── repository_impl/  # implement các interface repository của domain
│   │   ├── external/         # gọi service ngoài, api bên ngoài
│   │   └── __init__.py
│   └── utils/                # helper chung, thư viện tiện ích
│   └── rag/
│   │   ├── __init__.py
│   │   ├── pipelines/
│   │   │   ├── __init__.py
│   │   │   ├── embedding_pipeline.py     # Embedding + store
│   │   │   ├── retrieval_pipeline.py     # Vector search logic
│   │   │   └── generation_pipeline.py    # LLM response + synthesis
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── rag_service.py            # Orchestrator RAGService
│   │   │
│   │   ├── adapters/
│   │   │   ├── __init__.py
│   │   │   ├── langchain_adapter.py      # Nếu dùng LangChain
│   │   │   ├── openai_adapter.py         # Gọi model từ OpenAI API
│   │   │   └── vectorstore_adapter.py    # pgvector / chroma / FAISS
│   │   │
│   │   └── schemas/
│   │       ├── __init__.py
│   │       └── rag_schema.py             # Request/Response cho API
└── tests/                   # unit/integration tests
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

Read [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

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

Distributed under the MIT License. See `LICENSE` for more information.

---

## 💫 Author

**Lê Công**  
GitHub: [@baocong130899](https://github.com/baocong130899)  
Email: [lebaocongct@gmail.com](mailto:lebaocongct@gmail.com)

---

## 📝 Last Updated

*Last updated: 2025-10-18*