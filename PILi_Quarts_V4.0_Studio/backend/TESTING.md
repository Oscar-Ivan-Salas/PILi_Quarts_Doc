# Testing Guide - PILi Quarts Backend

## 🧪 Test Suite Overview

Comprehensive test suite following **testing-patterns** skill principles:
- **Testing Pyramid**: Many unit tests, some integration tests, few E2E tests
- **AAA Pattern**: Arrange, Act, Assert
- **Fast, Isolated, Repeatable**: All tests follow FIRST principles

---

## 📊 Test Coverage

### Test Files

| File | Tests | Coverage | Description |
|------|-------|----------|-------------|
| `test_pili_brain.py` | 15+ | PILI Brain | Unit tests for AI chat logic |
| `test_documents.py` | 20+ | Document Gen | PDF, Word, Excel generators |
| `test_auth.py` | 15+ | Auth | JWT, password hashing, tokens |
| `test_api_integration.py` | 20+ | API | Integration tests for endpoints |
| `conftest.py` | - | Fixtures | Shared fixtures and factories |

**Total Tests**: 70+  
**Target Coverage**: 80%+

---

## 🚀 Running Tests

### Quick Start

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=modules --cov-report=html

# Run specific test type
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m slow          # Slow tests only
```

### Using Test Runner Script

```bash
# Run all tests with coverage
python run_tests.py

# Run only unit tests
python run_tests.py --type unit

# Run without coverage
python run_tests.py --no-coverage

# Quiet mode
python run_tests.py --quiet
```

---

## 📁 Test Structure

```
tests/
├── __init__.py                  # Package init
├── conftest.py                  # Fixtures and configuration
├── test_pili_brain.py          # PILI AI unit tests
├── test_documents.py           # Document generator tests
├── test_auth.py                # Authentication tests
└── test_api_integration.py     # API integration tests
```

---

## 🔧 Fixtures

### Database Fixtures

```python
def test_with_database(db_session):
    """Use database session"""
    # db_session is automatically created and cleaned up
    pass
```

### API Client Fixtures

```python
async def test_api_endpoint(async_client):
    """Test API with async client"""
    response = await async_client.get("/api/endpoint")
    assert response.status_code == 200
```

### Factory Fixtures

```python
def test_with_user(user_factory):
    """Create test user"""
    user = user_factory(email="test@example.com")
    assert user.email == "test@example.com"
```

Available factories:
- `user_factory` - Create test users
- `workspace_factory` - Create workspaces
- `proyecto_factory` - Create projects

### Mock Fixtures

```python
def test_with_mock_gemini(mock_gemini_service):
    """Use mocked Gemini service"""
    # Gemini API calls are mocked
    pass
```

---

## ✅ Test Examples

### Unit Test Example

```python
@pytest.mark.unit
async def test_process_message_success(pili_brain, mock_gemini_service):
    """Should process message and return response"""
    # Arrange
    user_id = "test-user-123"
    message = "Test message"
    
    # Act
    result = await pili_brain.process_message(user_id, message)
    
    # Assert
    assert result is not None
    assert "response" in result
```

### Integration Test Example

```python
@pytest.mark.integration
async def test_chat_endpoint(async_client):
    """Should process chat request"""
    # Arrange
    payload = {"message": "Test", "context": {}}
    
    # Act
    response = await async_client.post("/api/pili/chat", json=payload)
    
    # Assert
    assert response.status_code == 200
    assert "response" in response.json()
```

---

## 🎯 Test Markers

Use markers to categorize tests:

```python
@pytest.mark.unit          # Fast, isolated unit tests
@pytest.mark.integration   # Integration tests with external deps
@pytest.mark.slow          # Slow tests (E2E, load tests)
@pytest.mark.asyncio       # Async tests
```

Run specific markers:

```bash
pytest -m unit              # Only unit tests
pytest -m "not slow"        # Exclude slow tests
pytest -m "unit or integration"  # Multiple markers
```

---

## 📈 Coverage Reports

### Generate Coverage

```bash
# HTML report
pytest --cov=modules --cov-report=html

# Terminal report
pytest --cov=modules --cov-report=term

# Both
pytest --cov=modules --cov-report=html --cov-report=term-missing
```

### View Coverage

```bash
# Open HTML report
open htmlcov/index.html  # macOS
start htmlcov/index.html # Windows
xdg-open htmlcov/index.html # Linux
```

### Coverage Requirements

- **Minimum**: 80% overall coverage
- **Critical modules**: 90%+ coverage
  - `modules/integration/auth/` (security)
  - `modules/pili/core/` (core logic)

---

## 🧹 Best Practices

### 1. Test Naming

```python
# ✅ Good - Descriptive
def test_process_message_with_empty_string_raises_error():
    pass

# ❌ Bad - Vague
def test_message():
    pass
```

### 2. AAA Pattern

```python
def test_example():
    # Arrange - Setup
    user = create_user()
    
    # Act - Execute
    result = process(user)
    
    # Assert - Verify
    assert result.success
```

### 3. One Assert Per Test

```python
# ✅ Good
def test_user_email():
    user = create_user()
    assert user.email == "test@example.com"

def test_user_name():
    user = create_user()
    assert user.name == "Test User"

# ❌ Bad - Multiple unrelated asserts
def test_user():
    user = create_user()
    assert user.email == "test@example.com"
    assert user.name == "Test User"
    assert user.role == "member"
```

### 4. Use Factories

```python
# ✅ Good - Use factory
def test_with_user(user_factory):
    user = user_factory(email="custom@example.com")
    assert user.email == "custom@example.com"

# ❌ Bad - Manual creation
def test_with_user(db_session):
    user = User(email="test@example.com", ...)
    db_session.add(user)
    db_session.commit()
```

### 5. Mock External Services

```python
# ✅ Good - Mock external API
def test_with_mock(mock_gemini_service):
    # Gemini API is mocked
    pass

# ❌ Bad - Real API calls in tests
def test_with_real_api():
    # Don't make real API calls!
    pass
```

---

## 🐛 Debugging Tests

### Run Single Test

```bash
# Run specific test file
pytest tests/test_pili_brain.py

# Run specific test class
pytest tests/test_pili_brain.py::TestPILIBrain

# Run specific test function
pytest tests/test_pili_brain.py::TestPILIBrain::test_process_message_success
```

### Verbose Output

```bash
# More verbose
pytest -v

# Even more verbose
pytest -vv

# Show print statements
pytest -s
```

### Stop on First Failure

```bash
pytest -x  # Stop on first failure
pytest --maxfail=3  # Stop after 3 failures
```

### Run Last Failed Tests

```bash
pytest --lf  # Last failed
pytest --ff  # Failed first, then others
```

---

## 🔍 Common Issues

### Issue: Import Errors

**Solution**: Make sure you're in the backend directory:

```bash
cd workspace-modern/backend
pytest
```

### Issue: Database Errors

**Solution**: Tests use in-memory SQLite, no setup needed. If issues persist, check `conftest.py`.

### Issue: Async Tests Failing

**Solution**: Make sure to use `@pytest.mark.asyncio`:

```python
@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result
```

---

## 📝 Adding New Tests

### 1. Create Test File

```python
# tests/test_new_feature.py
import pytest

@pytest.mark.unit
class TestNewFeature:
    def test_something(self):
        # Arrange
        # Act
        # Assert
        pass
```

### 2. Add Fixtures if Needed

```python
# tests/conftest.py
@pytest.fixture
def new_fixture():
    return "test data"
```

### 3. Run Tests

```bash
pytest tests/test_new_feature.py
```

---

## 🎓 Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- Testing Patterns Skill: `.agent/skills/testing-patterns/SKILL.md`

---

**Happy Testing! 🧪**
