"""
Integration Tests for API Endpoints
Following testing-patterns: Integration testing, API testing
"""
import pytest
from fastapi import status


@pytest.mark.integration
@pytest.mark.asyncio
class TestPILIAPIEndpoints:
    """
    PILI AI API integration tests.
    
    Following testing-patterns: Test API contracts
    """
    
    async def test_chat_endpoint_success(self, async_client):
        """Should process chat message and return response"""
        # Arrange
        payload = {
            "message": "Necesito cotización para instalación eléctrica",
            "context": {}
        }
        
        # Act
        response = await async_client.post("/api/pili/chat", json=payload)
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "response" in data
        assert "timestamp" in data
        assert "suggestions" in data
    
    async def test_chat_endpoint_empty_message_returns_error(self, async_client):
        """Should return 400 for empty message"""
        # Arrange
        payload = {"message": "", "context": {}}
        
        # Act
        response = await async_client.post("/api/pili/chat", json=payload)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    async def test_chat_endpoint_missing_message_returns_error(self, async_client):
        """Should return 422 for missing message field"""
        # Arrange
        payload = {"context": {}}  # Missing 'message'
        
        # Act
        response = await async_client.post("/api/pili/chat", json=payload)
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    async def test_get_history_endpoint(self, async_client):
        """Should return conversation history"""
        # Arrange
        user_id = "test-user-123"
        
        # Send a message first
        await async_client.post(
            "/api/pili/chat",
            json={"message": "Test message", "context": {}}
        )
        
        # Act
        response = await async_client.get(f"/api/pili/history/{user_id}")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "history" in data
        assert isinstance(data["history"], list)
    
    async def test_clear_history_endpoint(self, async_client):
        """Should clear conversation history"""
        # Arrange
        user_id = "test-user-123"
        
        # Send a message first
        await async_client.post(
            "/api/pili/chat",
            json={"message": "Test message", "context": {}}
        )
        
        # Act
        response = await async_client.delete(f"/api/pili/history/{user_id}")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == "History cleared"
    
    async def test_stats_endpoint(self, async_client):
        """Should return PILI statistics"""
        # Act
        response = await async_client.get("/api/pili/stats")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "active_conversations" in data
        assert "total_messages" in data
    
    async def test_health_endpoint(self, async_client):
        """Should return health status"""
        # Act
        response = await async_client.get("/api/pili/health")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data


@pytest.mark.integration
class TestRootEndpoints:
    """Root endpoint integration tests"""
    
    def test_root_endpoint(self, client):
        """Should return API information"""
        # Act
        response = client.get("/")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["service"] == "PILi Quarts API"
        assert "version" in data
        assert "docs" in data
    
    def test_health_check_endpoint(self, client):
        """Should return healthy status"""
        # Act
        response = client.get("/health")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_api_info_endpoint(self, client):
        """Should return API information"""
        # Act
        response = client.get("/api/info")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "modules" in data
        assert "features" in data
        assert "pili_ai" in data["modules"]


@pytest.mark.integration
class TestMiddleware:
    """Middleware integration tests"""
    
    def test_cors_headers_present(self, client):
        """Should include CORS headers"""
        # Act
        response = client.options("/")
        
        # Assert
        assert "access-control-allow-origin" in response.headers
    
    def test_security_headers_present(self, client):
        """Should include security headers"""
        # Act
        response = client.get("/")
        
        # Assert
        assert "x-content-type-options" in response.headers
        assert response.headers["x-content-type-options"] == "nosniff"
        assert "x-frame-options" in response.headers
        assert response.headers["x-frame-options"] == "DENY"
    
    def test_request_id_header_present(self, client):
        """Should include request ID header"""
        # Act
        response = client.get("/")
        
        # Assert
        assert "x-request-id" in response.headers
        assert len(response.headers["x-request-id"]) > 0
    
    def test_process_time_header_present(self, client):
        """Should include process time header"""
        # Act
        response = client.get("/")
        
        # Assert
        assert "x-process-time" in response.headers
        assert "s" in response.headers["x-process-time"]  # Format: "0.123s"
    
    def test_rate_limit_headers_present(self, client):
        """Should include rate limit headers"""
        # Act
        response = client.get("/")
        
        # Assert
        assert "x-ratelimit-limit" in response.headers
        assert "x-ratelimit-remaining" in response.headers
        assert "x-ratelimit-reset" in response.headers
    
    @pytest.mark.slow
    def test_rate_limiting_enforced(self, client):
        """Should enforce rate limiting"""
        # Arrange
        limit = 60  # Default limit
        
        # Act - Make requests beyond limit
        responses = []
        for i in range(limit + 5):
            response = client.get("/")
            responses.append(response)
        
        # Assert - Last requests should be rate limited
        assert any(r.status_code == status.HTTP_429_TOO_MANY_REQUESTS for r in responses[-5:])


@pytest.mark.integration
class TestErrorHandling:
    """Error handling integration tests"""
    
    def test_404_error_format(self, client):
        """Should return formatted 404 error"""
        # Act
        response = client.get("/nonexistent-endpoint")
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "error" in data
        assert data["error"] == "NotFound"
        assert "message" in data
        assert "path" in data
    
    def test_422_validation_error_format(self, client):
        """Should return formatted validation error"""
        # Act - Send invalid JSON
        response = client.post(
            "/api/pili/chat",
            json={"invalid_field": "value"}  # Missing required 'message'
        )
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()
        assert "detail" in data  # FastAPI validation error format
