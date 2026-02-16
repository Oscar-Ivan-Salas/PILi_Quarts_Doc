# PILi Quarts Backend

Enterprise-grade construction project management and quotation system backend.

## 🚀 Features

- **PILI AI Module**: AI-powered chat with Gemini, data extraction, WebSocket real-time
- **Document Generation**: Professional PDF, Word, Excel documents
- **Database**: PostgreSQL with SQLAlchemy ORM, versioning, audit logs
- **Authentication**: JWT with bcrypt, RBAC with 5 roles and 25+ permissions
- **Security**: Rate limiting, security headers, CORS, input validation
- **Monitoring**: Request logging, metrics, health checks

## 📦 Tech Stack

- **Framework**: FastAPI 0.109 (async, OpenAPI docs)
- **Database**: PostgreSQL + SQLAlchemy 2.0
- **AI**: Google Gemini AI
- **Documents**: ReportLab (PDF), python-docx (Word), openpyxl (Excel)
- **Auth**: JWT (python-jose), bcrypt (passlib)
- **Validation**: Pydantic v2
- **Testing**: pytest, pytest-asyncio

## 🛠️ Installation

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Redis (optional, for caching)

### Setup

1. **Clone and navigate**:
   ```bash
   cd workspace-modern/backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**:
   ```bash
   # Database will be auto-created on first run
   # Or run migrations manually:
   alembic upgrade head
   ```

## 🚀 Running

### Development

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📚 API Documentation

Once running, visit:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

## 🏗️ Project Structure

```
backend/
├── main.py                     # FastAPI application entry point
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
│
├── modules/                   # Modular architecture
│   ├── database/             # Database module
│   │   ├── base.py          # SQLAlchemy base
│   │   ├── models/          # Database models
│   │   │   ├── user.py
│   │   │   ├── workspace.py
│   │   │   ├── proyecto.py
│   │   │   ├── documento.py
│   │   │   └── ...
│   │   └── schemas/         # Pydantic schemas
│   │
│   ├── pili/                # PILI AI module
│   │   ├── config/          # Configuration
│   │   ├── core/            # Core logic
│   │   │   ├── brain.py    # PILI Brain
│   │   │   └── gemini.py   # Gemini service
│   │   └── api/             # API endpoints
│   │       ├── router.py   # REST endpoints
│   │       ├── schemas.py  # Request/response models
│   │       └── websocket.py # WebSocket endpoint
│   │
│   ├── documents/           # Document generation module
│   │   ├── generators/     # Document generators
│   │   │   ├── pdf_generator.py
│   │   │   ├── word_generator.py
│   │   │   └── excel_generator.py
│   │   └── service.py      # Main service
│   │
│   └── integration/         # Integration module
│       ├── auth/           # Authentication
│       │   ├── jwt.py     # JWT logic
│       │   └── permissions.py # RBAC
│       └── middleware/     # Middleware
│           ├── rate_limit.py
│           └── logging.py
│
└── tests/                  # Test suite
    ├── test_pili.py
    ├── test_documents.py
    └── test_auth.py
```

## 🔐 Environment Variables

Key environment variables (see `.env.example` for complete list):

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/pili_quarts

# AI
PILI_GEMINI_API_KEY=your-api-key

# Auth
SECRET_KEY=your-secret-key

# Server
HOST=0.0.0.0
PORT=8000
```

## 🧪 Testing

Run tests:

```bash
pytest
```

With coverage:

```bash
pytest --cov=modules --cov-report=html
```

## 📊 Modules

### 1. PILI AI Module

AI-powered chat and data extraction:

- **Endpoints**: `/api/pili/chat`, `/api/pili/history/{user_id}`
- **WebSocket**: `/ws/pili/{user_id}`
- **Features**: Retry logic, rate limiting, metrics, conversation history

### 2. Document Generator Module

Professional document generation:

- **Formats**: PDF, Word, Excel
- **Types**: Cotizaciones, Informes, Presupuestos
- **Libraries**: ReportLab, python-docx, openpyxl

### 3. Database Module

PostgreSQL with SQLAlchemy:

- **Models**: User, Workspace, Proyecto, Documento, Folder, etc.
- **Features**: Versioning, audit logs, relationships

### 4. Integration Module

Authentication and middleware:

- **Auth**: JWT with bcrypt, RBAC (5 roles, 25+ permissions)
- **Middleware**: Rate limiting, logging, security headers, CORS

## 🔒 Security Features

- JWT authentication with refresh tokens
- Password hashing with bcrypt
- Role-based access control (RBAC)
- Rate limiting (sliding window algorithm)
- Security headers (CSP, HSTS, X-Frame-Options, etc.)
- Input validation with Pydantic
- SQL injection protection (SQLAlchemy)
- CORS configuration

## 📈 Performance

- Async/await throughout
- Connection pooling (PostgreSQL)
- Request caching (Redis, optional)
- Rate limiting
- Efficient database queries

## 🚢 Deployment

### Docker (Recommended)

```bash
docker build -t pili-quarts-backend .
docker run -p 8000:8000 --env-file .env pili-quarts-backend
```

### Manual

```bash
# Install dependencies
pip install -r requirements.txt

# Run with gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 📝 License

Proprietary - PILi Quarts

## 👥 Team

Built with enterprise-grade standards following clean-code, python-patterns, architecture, and deployment-procedures best practices.
