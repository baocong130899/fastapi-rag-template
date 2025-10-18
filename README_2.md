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





| Phần cấu hình                                                                   | Directive / command                          | Giải thích (tiếng Việt)                                                                                                                                                             |
| ------------------------------------------------------------------------------- | -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `events { worker_connections 1024; }`                                           | `worker_connections`                         | Mỗi worker process Nginx có thể xử lý tối đa 1024 kết nối đồng thời.                                                                                                                |
| `resolver 127.0.0.11 ipv6=off valid=30s;`                                       | `resolver`                                   | Cho phép Nginx resolve tên miền (ví dụ “rag”) bằng DNS nội bộ Docker (127.0.0.11). `ipv6=off` tắt IPv6 lookup. `valid=30s` là thời gian cache kết quả DNS.                          |
| `client_max_body_size 100M;`                                                    | `client_max_body_size`                       | Giới hạn kích thước upload request body (ví dụ file upload) tối đa 100MB.                                                                                                           |
| `upstream rag { server rag:8000; }`                                             | `upstream`                                   | Định nghĩa backend group tên “rag” chứa backend server là `rag:8000`.                                                                                                               |
| `map $http_upgrade $connection_upgrade { default upgrade; "" close; }`          | `map`                                        | Dùng để ánh xạ header `Upgrade` từ client sang biến `$connection_upgrade`. Nếu client gửi `Upgrade`, biến sẽ là `upgrade`, nếu không thì `close`. Dùng sau này khi proxy WebSocket. |
| `server { listen 80 default_server; server_name _; … }`                         | `listen`, `server_name`                      | `listen 80` để lắng cổng 80; `default_server` để block này là mặc định nếu không có server_name khớp; `server_name _;` dùng ký hiệu `_` để match tất cả host names.                 |
| `add_header 'Access-Control-Allow-Origin' '*' always;` và các `add_header` khác | `add_header`                                 | Thêm header CORS vào response để cho phép client từ domain khác gửi request. `always` đảm bảo header được gửi cả khi lỗi HTTP.                                                      |
| `if ($request_method = OPTIONS) { … return 204; }`                              | `if`, `return`                               | Xử lý preflight request (OPTIONS) của CORS, trả về mã 204 No Content nhanh.                                                                                                         |
| `location /api { … }`                                                           | `location`                                   | Bắt các request URIs bắt đầu `/api` và định nghĩa cách proxy chúng.                                                                                                                 |
| `proxy_pass http://rag/api;`                                                    | `proxy_pass`                                 | Chuyển request tới backend upstream “rag”, cụ thể là tới path `/api`.                                                                                                               |
| `proxy_http_version 1.1;`                                                       | `proxy_http_version`                         | Sử dụng HTTP/1.1 khi proxy tới backend — cần cho WebSocket / keep-alive.                                                                                                            |
| `proxy_set_header Host $host;`                                                  | `proxy_set_header`                           | Gửi header Host gốc của client đến backend, để backend biết tên host client truy vấn.                                                                                               |
| `proxy_set_header X-Real-IP $remote_addr;`                                      | `proxy_set_header`                           | Gửi IP thật của client đến backend.                                                                                                                                                 |
| `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;`                  | `proxy_set_header`                           | Gửi chuỗi các IP đã qua (nếu có proxy trung gian) đến backend.                                                                                                                      |
| `proxy_set_header X-Forwarded-Proto $scheme;`                                   | `proxy_set_header`                           | Gửi giao thức (http / https) gốc từ client đến backend.                                                                                                                             |
| `proxy_set_header Upgrade $http_upgrade;`                                       | `proxy_set_header`                           | Nếu client gửi header Upgrade (ví dụ WebSocket), truyền tiếp header này đến backend.                                                                                                |
| `proxy_set_header Connection $connection_upgrade;`                              | `proxy_set_header`                           | Dùng biến `$connection_upgrade` từ `map` để quyết định gửi `Connection: upgrade` hay `close`.                                                                                       |
| `proxy_buffering off;`                                                          | `proxy_buffering`                            | Tắt việc Nginx buffer response từ backend, để đẩy dữ liệu nhanh hơn đến client (dùng cho streaming, SSE, WebSocket, etc.).                                                          |
| `proxy_read_timeout 300s; proxy_send_timeout 300s;`                             | `proxy_read_timeout`, `proxy_send_timeout`   | Thời gian tối đa Nginx chờ đọc / gửi dữ liệu từ backend / tới client trước khi timeout. 300 giây (5 phút).                                                                          |
| `proxy_intercept_errors off;`                                                   | `proxy_intercept_errors`                     | Nếu backend trả lỗi (404, 500...), Nginx không “can thiệp” để hiện trang lỗi riêng mà để lỗi từ backend truyền về client.                                                           |
| Các `location /redoc` và `location /openapi.json`                               | `location`, `proxy_pass`, `proxy_set_header` | Tương tự block `/api`, nhưng dành cho các đường dẫn tài liệu API — proxy traffic đến backend tương ứng (ví dụ `/redoc`, `/openapi.json`).                                           |
