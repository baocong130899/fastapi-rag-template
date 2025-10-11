uv sync --link-mode=copy
uvicorn app.main:app --reload

alembic init -t async migration
alembic revision --autogenerate -m "init_ table"
alembic upgrade head

Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\.venv\Scripts\Activate.ps1



my_project/
├── src/                    # mã nguồn chính
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
└── tests/                   # unit/integration tests
    ├── domain/
    ├── application/
    └── presentation/


| Thư mục            | Nội dung / trách nhiệm                                                                                                                                                                |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **main.py**        | Tạo FastAPI app, gắn routers, cấu hình middleware, startup/shutdown events.                                                                                                           |
| **config**         | Cài đặt config (ví dụ lấy từ `.env`), cấu hình logging, cấu hình CORS, các thiết lập chung.                                                                                           |
| **presentation**   | Tầng tiếp xúc với HTTP: routers, controllers, schemas để nhận request / trả response. Chỉ xử lý việc đưa nhận dữ liệu, không chứa logic nghiệp vụ nặng.                               |
| **application**    | Các dịch vụ ứng dụng (use cases), phối hợp domain, orchestrate các repository, domain services, validate cao hơn nếu cần.                                                             |
| **domain**         | Tầng cốt lõi: các khái niệm của nghiệp vụ, mô hình hóa domain: Entity, ValueObject, Aggregates, các interface (repository), events, invariants. Không biết gì về HTTP, DB, framework. |
| **infrastructure** | Làm việc với DB (ví dụ SQLAlchemy, Tortoise, hoặc async ORM), triển khai interface repository, bên ngoài như dịch vụ gửi email, lưu file, caching, etc.                               |
| **utils**          | Các helper, chức năng dùng chung (ví dụ format error, mã hóa, validate bổ sung…)                                                                                                      |


🔁 Luồng hoạt động (Flow)
Request → Presentation (API)
        → Application (Use Case)
        → Domain (Business Logic)
        → Infrastructure (Persistence / External)

Khi trả dữ liệu:
Infrastructure → Domain → Application → Presentation → Response


src/
│   __init__.py
│   main.py
│   container.py
│
├── config/
│   └── __init__.py
│
├── domain/
│   ├── __init__.py
│   ├── entities/
│   │   └── __init__.py
│   └── repositories/
│       └── __init__.py
│
├── application/
│   └── __init__.py
│   └── services/
│       └── __init__.py
│
├── infrastructure/
│   ├── __init__.py
│   ├── database.py
│   ├── models/
│   │   └── __init__.py
│   └── repository_impl/
│       └── __init__.py
│
└── presentation/
    ├── __init__.py
    ├── api/
    │   └── v1/
    │       ├── __init__.py
    │       └── endpoints/
    │           └── __init__.py
    └── schemas/
        └── __init__.py



src/
├── main.py
├── container.py
├── config/
│   └── settings.py
│
├── domain/
│   ├── entities/
│   ├── repositories/
│   └── __init__.py
│
├── application/
│   ├── services/
│   └── __init__.py
│
├── infrastructure/
│   ├── database.py
│   ├── repository_impl/
│   ├── models/
│   └── __init__.py
│
├── presentation/
│   ├── api/v1/endpoints/
│   ├── schemas/
│   └── __init__.py
│
└── rag/
    ├── __init__.py
    ├── pipelines/
    │   ├── __init__.py
    │   ├── embedding_pipeline.py     # Embedding + store
    │   ├── retrieval_pipeline.py     # Vector search logic
    │   └── generation_pipeline.py    # LLM response + synthesis
    │
    ├── services/
    │   ├── __init__.py
    │   └── rag_service.py            # Orchestrator RAGService
    │
    ├── adapters/
    │   ├── __init__.py
    │   ├── langchain_adapter.py      # Nếu dùng LangChain
    │   ├── openai_adapter.py         # Gọi model từ OpenAI API
    │   └── vectorstore_adapter.py    # pgvector / chroma / FAISS
    │
    └── schemas/
        ├── __init__.py
        └── rag_schema.py             # Request/Response cho API
