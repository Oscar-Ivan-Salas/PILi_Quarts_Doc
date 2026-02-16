"""
Unit Tests for PILI Brain
Following testing-patterns: AAA pattern, unit test principles
"""
import pytest
from unittest.mock import AsyncMock, Mock
from datetime import datetime

from modules.pili.core.brain import PILIBrain


@pytest.mark.unit
@pytest.mark.asyncio
class TestPILIBrain:
    """
    PILI Brain unit tests.
    
    Following testing-patterns: Group related tests
    """
    
    async def test_process_message_success(self, pili_brain, mock_gemini_service):
        """
        Should process message and return response.
        
        Following testing-patterns: AAA pattern
        """
        # Arrange
        user_id = "test-user-123"
        message = "Necesito cotización para instalación eléctrica"
        
        # Act
        result = await pili_brain.process_message(user_id, message)
        
        # Assert
        assert result is not None
        assert "response" in result
        assert result["response"] == "Mocked AI response"
        assert "timestamp" in result
        assert "suggestions" in result
        
        # Verify Gemini was called
        mock_gemini_service.generate_response.assert_called_once()
    
    async def test_process_message_empty_raises_error(self, pili_brain):
        """
        Should raise ValueError for empty message.
        
        Following testing-patterns: Test edge cases
        """
        # Arrange
        user_id = "test-user-123"
        empty_message = ""
        
        # Act & Assert
        with pytest.raises(ValueError, match="Message cannot be empty"):
            await pili_brain.process_message(user_id, empty_message)
    
    async def test_process_message_whitespace_raises_error(self, pili_brain):
        """
        Should raise ValueError for whitespace-only message.
        
        Following testing-patterns: Test edge cases
        """
        # Arrange
        user_id = "test-user-123"
        whitespace_message = "   \n\t   "
        
        # Act & Assert
        with pytest.raises(ValueError, match="Message cannot be empty"):
            await pili_brain.process_message(user_id, whitespace_message)
    
    async def test_process_message_with_context(self, pili_brain, mock_gemini_service):
        """
        Should include context in prompt.
        
        Following testing-patterns: Test with different inputs
        """
        # Arrange
        user_id = "test-user-123"
        message = "¿Cuánto cuesta?"
        context = {
            "proyecto_id": "proj-123",
            "tipo_servicio": "electricidad"
        }
        
        # Act
        result = await pili_brain.process_message(user_id, message, context)
        
        # Assert
        assert result is not None
        assert result["response"] == "Mocked AI response"
        
        # Verify context was used in prompt
        call_args = mock_gemini_service.generate_response.call_args
        prompt = call_args[0][0]
        assert "proyecto_id" in prompt
        assert "electricidad" in prompt
    
    async def test_conversation_history_tracking(self, pili_brain):
        """
        Should track conversation history.
        
        Following testing-patterns: Test state changes
        """
        # Arrange
        user_id = "test-user-123"
        
        # Act - Send multiple messages
        await pili_brain.process_message(user_id, "Mensaje 1")
        await pili_brain.process_message(user_id, "Mensaje 2")
        
        # Assert
        history = pili_brain._get_history(user_id)
        assert len(history) == 2
        assert history[0]["user"] == "Mensaje 1"
        assert history[1]["user"] == "Mensaje 2"
    
    async def test_history_limit(self, pili_brain, mock_gemini_service):
        """
        Should limit history to max size.
        
        Following testing-patterns: Test boundaries
        """
        # Arrange
        user_id = "test-user-123"
        max_history = pili_brain.gemini.settings.pili_max_history if hasattr(pili_brain.gemini, 'settings') else 50
        
        # Act - Send more messages than limit
        for i in range(max_history + 10):
            await pili_brain.process_message(user_id, f"Message {i}")
        
        # Assert
        history = pili_brain._get_history(user_id)
        assert len(pili_brain.conversation_history[user_id]) <= max_history
    
    def test_clear_history(self, pili_brain):
        """
        Should clear user history.
        
        Following testing-patterns: Test cleanup
        """
        # Arrange
        user_id = "test-user-123"
        pili_brain.conversation_history[user_id] = [
            {"user": "msg1", "assistant": "resp1", "timestamp": datetime.utcnow().isoformat()}
        ]
        
        # Act
        pili_brain.clear_history(user_id)
        
        # Assert
        assert user_id not in pili_brain.conversation_history
    
    def test_get_stats(self, pili_brain):
        """
        Should return brain statistics.
        
        Following testing-patterns: Test behavior
        """
        # Arrange
        pili_brain.conversation_history["user1"] = [{"user": "msg", "assistant": "resp", "timestamp": ""}]
        pili_brain.conversation_history["user2"] = [{"user": "msg", "assistant": "resp", "timestamp": ""}]
        
        # Act
        stats = pili_brain.get_stats()
        
        # Assert
        assert stats["active_conversations"] == 2
        assert stats["total_messages"] == 2
        assert "settings" in stats
    
    async def test_graceful_degradation_on_error(self, pili_brain, mock_gemini_service):
        """
        Should return fallback response on error.
        
        Following testing-patterns: Test error handling
        """
        # Arrange
        user_id = "test-user-123"
        message = "Test message"
        
        # Mock Gemini to raise error
        mock_gemini_service.generate_response.side_effect = Exception("API Error")
        
        # Act
        result = await pili_brain.process_message(user_id, message)
        
        # Assert
        assert result is not None
        assert "error" in result
        assert "Lo siento" in result["response"]  # Fallback message
    
    async def test_timeout_handling(self, pili_brain, mock_gemini_service):
        """
        Should handle timeout errors.
        
        Following testing-patterns: Test timeout scenarios
        """
        # Arrange
        user_id = "test-user-123"
        message = "Test message"
        
        # Mock slow response
        import asyncio
        async def slow_response(*args, **kwargs):
            await asyncio.sleep(100)  # Longer than timeout
            return "Response"
        
        mock_gemini_service.generate_response = slow_response
        
        # Act & Assert
        with pytest.raises(TimeoutError):
            await pili_brain.process_message(user_id, message)


@pytest.mark.unit
class TestPILIBrainHelpers:
    """
    Test PILI Brain helper methods.
    
    Following testing-patterns: Test internal logic
    """
    
    def test_build_prompt_basic(self, pili_brain):
        """Should build basic prompt"""
        # Arrange
        message = "Test message"
        history = []
        context = None
        
        # Act
        prompt = pili_brain._build_prompt(message, history, context)
        
        # Assert
        assert "PILI" in prompt
        assert "Test message" in prompt
        assert "Usuario:" in prompt
    
    def test_build_prompt_with_history(self, pili_brain):
        """Should include history in prompt"""
        # Arrange
        message = "New message"
        history = [
            {"user": "Old message", "assistant": "Old response"}
        ]
        context = None
        
        # Act
        prompt = pili_brain._build_prompt(message, history, context)
        
        # Assert
        assert "Old message" in prompt
        assert "Old response" in prompt
        assert "New message" in prompt
    
    def test_generate_suggestions_electricidad(self, pili_brain):
        """Should generate relevant suggestions for electricidad"""
        # Arrange
        context = {"tipo_servicio": "electricidad"}
        extracted_data = None
        
        # Act
        suggestions = pili_brain._generate_suggestions(context, extracted_data)
        
        # Assert
        assert len(suggestions) > 0
        assert len(suggestions) <= 3  # Max 3 suggestions
        assert any("puesta a tierra" in s.lower() for s in suggestions)
