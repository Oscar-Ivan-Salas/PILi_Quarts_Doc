"""
Test Configuration and Fixtures
Following testing-patterns: Shared fixtures and setup
"""
import pytest
import asyncio
from typing import Generator, AsyncGenerator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from httpx import AsyncClient

from modules.database.base import Base, get_session
from modules.pili.core.brain import PILIBrain
from modules.pili.core.gemini import GeminiService
from main import app


# ============================================================================
# DATABASE FIXTURES
# ============================================================================

@pytest.fixture(scope="session")
def test_db_engine():
    """
    Create test database engine.
    
    Following testing-patterns: Session-scoped database
    """
    # Use in-memory SQLite for tests
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Cleanup
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(test_db_engine) -> Generator[Session, None, None]:
    """
    Create database session for each test.
    
    Following testing-patterns: Function-scoped session with cleanup
    """
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_db_engine
    )
    
    session = SessionLocal()
    
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# ============================================================================
# API CLIENT FIXTURES
# ============================================================================

@pytest.fixture(scope="function")
def client(db_session) -> Generator[TestClient, None, None]:
    """
    Create FastAPI test client.
    
    Following testing-patterns: Override dependencies
    """
    # Override database dependency
    def override_get_session():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_session] = override_get_session
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clear overrides
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
async def async_client(db_session) -> AsyncGenerator[AsyncClient, None]:
    """
    Create async HTTP client for testing.
    
    Following python-patterns: Async testing
    """
    # Override database dependency
    def override_get_session():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_session] = override_get_session
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


# ============================================================================
# PILI AI FIXTURES
# ============================================================================

@pytest.fixture(scope="function")
def mock_gemini_service(mocker):
    """
    Mock Gemini service for testing.
    
    Following testing-patterns: Mock external services
    """
    mock_service = mocker.Mock(spec=GeminiService)
    mock_service.generate_response = mocker.AsyncMock(
        return_value="Mocked AI response"
    )
    mock_service.get_metrics = mocker.Mock(
        return_value={
            "total_requests": 10,
            "total_errors": 0,
            "total_tokens": 1000
        }
    )
    return mock_service


@pytest.fixture(scope="function")
def pili_brain(mock_gemini_service):
    """
    Create PILI Brain instance for testing.
    
    Following testing-patterns: Fixture with dependencies
    """
    return PILIBrain(mock_gemini_service)


# ============================================================================
# TEST DATA FACTORIES
# ============================================================================

@pytest.fixture
def user_factory(db_session):
    """
    Factory for creating test users.
    
    Following testing-patterns: Factory pattern for test data
    """
    from modules.database.models import User
    from modules.integration.auth.jwt import hash_password
    
    def create_user(
        email: str = "test@example.com",
        nombre: str = "Test User",
        password: str = "password123",
        rol_global: str = "member"
    ) -> User:
        user = User(
            email=email,
            nombre=nombre,
            password_hash=hash_password(password),
            rol_global=rol_global,
            email_verified=True
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user
    
    return create_user


@pytest.fixture
def workspace_factory(db_session):
    """Factory for creating test workspaces"""
    from modules.database.models import Workspace
    
    def create_workspace(
        nombre: str = "Test Workspace",
        slug: str = "test-workspace",
        owner_id = None,
        plan: str = "free"
    ) -> Workspace:
        workspace = Workspace(
            nombre=nombre,
            slug=slug,
            owner_id=owner_id,
            plan=plan
        )
        db_session.add(workspace)
        db_session.commit()
        db_session.refresh(workspace)
        return workspace
    
    return create_workspace


@pytest.fixture
def proyecto_factory(db_session):
    """Factory for creating test projects"""
    from modules.database.models import Proyecto
    
    def create_proyecto(
        nombre: str = "Test Project",
        workspace_id = None,
        tipo: str = "residencial",
        estado: str = "activo"
    ) -> Proyecto:
        proyecto = Proyecto(
            nombre=nombre,
            workspace_id=workspace_id,
            tipo=tipo,
            estado=estado
        )
        db_session.add(proyecto)
        db_session.commit()
        db_session.refresh(proyecto)
        return proyecto
    
    return create_proyecto


# ============================================================================
# AUTHENTICATION FIXTURES
# ============================================================================

@pytest.fixture
def auth_headers(user_factory):
    """
    Create authentication headers for testing.
    
    Following testing-patterns: Authenticated test setup
    """
    from modules.integration.auth.jwt import create_tokens
    
    user = user_factory(email="auth@example.com", rol_global="admin")
    tokens = create_tokens(
        user_id=str(user.id),
        email=user.email,
        rol=user.rol_global
    )
    
    return {
        "Authorization": f"Bearer {tokens.access_token}"
    }


# ============================================================================
# DOCUMENT TEST DATA
# ============================================================================

@pytest.fixture
def cotizacion_data():
    """
    Sample quotation data for testing.
    
    Following testing-patterns: Realistic test data
    """
    return {
        "numero": "COT-2026-001",
        "fecha": "29/01/2026",
        "valida_hasta": "28/02/2026",
        "cliente": {
            "nombre": "Juan Pérez",
            "empresa": "Constructora ABC",
            "email": "juan@abc.com",
            "telefono": "+52 555 1234567",
            "direccion": "Calle Principal 123, CDMX"
        },
        "items": [
            {
                "descripcion": "Instalación eléctrica trifásica",
                "cantidad": 1,
                "precio_unitario": 50000.00,
                "subtotal": 50000.00
            },
            {
                "descripcion": "Tablero eléctrico 12 circuitos",
                "cantidad": 2,
                "precio_unitario": 8000.00,
                "subtotal": 16000.00
            }
        ],
        "totales": {
            "subtotal": 66000.00,
            "iva": 10560.00,
            "total": 76560.00
        },
        "terminos": "Pago: 50% anticipo, 50% contra entrega. Garantía: 12 meses.",
        "empresa_nombre": "PILi Engineering",
        "empresa_contacto": "contacto@pili.com"
    }


# ============================================================================
# PYTEST CONFIGURATION
# ============================================================================

@pytest.fixture(scope="session")
def event_loop():
    """
    Create event loop for async tests.
    
    Following python-patterns: Async testing setup
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


def pytest_configure(config):
    """
    Pytest configuration.
    
    Following testing-patterns: Test markers
    """
    config.addinivalue_line(
        "markers", "unit: Unit tests"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests"
    )
    config.addinivalue_line(
        "markers", "slow: Slow tests"
    )
    config.addinivalue_line(
        "markers", "asyncio: Async tests"
    )
