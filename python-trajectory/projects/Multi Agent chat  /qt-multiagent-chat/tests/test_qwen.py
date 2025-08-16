import pytest
from unittest.mock import Mock, patch
from services.llm_qwen import QwenProvider


class TestQwenProvider:
    def test_init_defaults(self):
        provider = QwenProvider()
        assert provider.model == "qwen2.5:7b-instruct"
        assert provider.host == "http://localhost:11434"
        assert provider.timeout == 120

    def test_init_custom(self):
        provider = QwenProvider(
            model="custom-model",
            host="http://example.com:8080/",
            timeout=60
        )
        assert provider.model == "custom-model"
        assert provider.host == "http://example.com:8080"
        assert provider.timeout == 60

    def test_name_property(self):
        provider = QwenProvider(model="test-model")
        assert provider.name == "ollama:test-model"

    @patch('requests.get')
    def test_health_success(self, mock_get):
        mock_get.return_value.ok = True
        provider = QwenProvider()
        assert provider.health() is True
        mock_get.assert_called_once_with("http://localhost:11434/api/tags", timeout=1.5)

    @patch('requests.get')
    def test_health_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection error")
        provider = QwenProvider()
        assert provider.health() is False

    @patch('requests.post')
    def test_complete_success(self, mock_post):
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {
            "message": {"content": "Test response"}
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        # Mock health check
        with patch.object(QwenProvider, 'health', return_value=True):
            provider = QwenProvider()
            result = provider.complete("System prompt", "User message")
            
        assert result == "Test response"
        mock_post.assert_called_once()

    def test_complete_unhealthy(self):
        with patch.object(QwenProvider, 'health', return_value=False):
            provider = QwenProvider()
            with pytest.raises(RuntimeError, match="Ollama is not reachable"):
                provider.complete("System", "User")
