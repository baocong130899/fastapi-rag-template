# 🚀 RAG Template – FastAPI + LangChain + PGVector

A **production-ready Retrieval-Augmented Generation (RAG)** template built with **FastAPI**, **LangChain**, and **PostgreSQL + PGVector**.  
This project provides a clean architecture for building LLM-powered applications with scalable vector search, modular pipelines, and easy deployment via Docker and Nginx.

---

## 🌟 Features

- 🔍 **RAG Architecture** – Combines vector retrieval + LLM generation  
- 🧩 **Modular Pipelines** – Embedding, retrieval, and generation separated cleanly  
- 🗃️ **PGVector Integration** – Store and search embeddings in PostgreSQL  
- ⚡ **FastAPI Backend** – High-performance async API for LLM apps  
- 🛠️ **Dockerized Deployment** – Ready-to-run with Nginx reverse proxy  
- 🧱 **Domain-Driven Design (DDD)** – Maintainable, scalable codebase  
- 📊 **Observability Ready** – Easily integrate with Langfuse / LangWatch / Prometheus  

---

## 🧰 Tech Stack

| Layer | Technology |
|--------|-------------|
| Backend API | [FastAPI](https://fastapi.tiangolo.com/) |
| LLM Framework | [LangChain](https://www.langchain.com/) |
| Vector DB | [PGVector](https://github.com/pgvector/pgvector) |
| Containerization | Docker + Docker Compose |
| Reverse Proxy | Nginx |
| Scheduler | APScheduler (async) |
| Monitoring | Optional: Langfuse, LangWatch |

---

## ⚙️ Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/baocong130899/rag.git
cd rag
git checkout develop
```

### 2️⃣ Setup environment
Create `.env` file:
```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=ragdb
OPENAI_API_KEY=your_openai_api_key
JWT_SECRET=your_secret
```

### 3️⃣ Run with Docker
```bash
docker-compose up -d --build
```

API available at → [http://localhost:8000](http://localhost:8000)

---

## 🧠 Project Structure

```
rag/
├── pipelines/
│   ├── embedding_pipeline.py
│   ├── retrieval_pipeline.py
│   └── generation_pipeline.py
│
├── services/
│   ├── vector_service.py
│   ├── document_service.py
│   └── llm_service.py
│
├── api/
│   ├── routers/
│   └── main.py
│
└── config/
    ├── settings.py
    ├── logger.py
    └── db.py
```

---

## 📡 API Endpoints (Examples)

| Endpoint | Method | Description |
|-----------|--------|-------------|
| `/api/v1/embed` | POST | Store document embeddings |
| `/api/v1/query` | POST | Retrieve and generate answer |
| `/api/v1/health` | GET | Health check endpoint |

---

## 🌍 Deployment

### 🐳 Docker Compose
This template includes:
- **FastAPI service**
- **PostgreSQL + PGVector**
- **Nginx reverse proxy** (CORS, HTTPS-ready)

### 🔁 Reverse Proxy Example
```nginx
add_header 'Access-Control-Allow-Origin' '*' always;
add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type' always;
```

---

## 🧩 Integration with Langfuse / LangWatch

You can integrate monitoring easily:
```bash
pip install langfuse
```
Then wrap pipelines to track LLM calls, latency, and cost.

---

## 📈 Future Roadmap

- [ ] Add Hybrid Search (BM25 + Vector)
- [ ] Add Authentication (JWT-based)
- [ ] Integrate OpenTelemetry tracing
- [ ] Add Streamlit frontend demo
- [ ] Add test coverage

---

## 🏷️ Topics

`rag`, `fastapi`, `langchain`, `pgvector`, `llm`,  
`retrieval-augmented-generation`, `vector-database`,  
`docker`, `nginx`, `openai`, `ai-backend`, `mlops`,  
`langfuse`, `langwatch`, `python`, `chatbot`, `template`

---

## 🪪 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 💫 Author

**Lê Công**  
GitHub: [@baocong130899](https://github.com/baocong130899)  
Email: lecong.dev@gmail.com  

---

## ⭐ Support

If you find this project useful, please **star** 🌟 the repository and consider contributing!
