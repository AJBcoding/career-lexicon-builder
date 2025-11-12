import pytest
from services.anthropic_service import AnthropicService
from unittest.mock import Mock, patch, AsyncMock


def test_invoke_skill():
    """Test synchronous skill invocation"""
    with patch('services.anthropic_service.Anthropic') as MockAnthropic:
        mock_client = Mock()
        MockAnthropic.return_value = mock_client

        mock_response = Mock()
        mock_response.content = [Mock(text="Test response")]
        mock_response.usage = Mock(input_tokens=10, output_tokens=20)
        mock_response.model = "claude-sonnet-4-20250514"
        mock_response.stop_reason = "end_turn"

        mock_client.messages.create.return_value = mock_response

        service = AnthropicService(api_key="test-key")
        result = service.invoke_skill("test-skill", "test prompt")

        assert result["success"] is True
        assert result["content"] == "Test response"
        assert result["usage"]["input_tokens"] == 10
        assert result["usage"]["output_tokens"] == 20
        assert result["model"] == "claude-sonnet-4-20250514"
        assert result["stop_reason"] == "end_turn"

        # Verify API was called correctly
        mock_client.messages.create.assert_called_once()
        call_args = mock_client.messages.create.call_args
        assert call_args.kwargs["model"] == "claude-sonnet-4-20250514"
        assert call_args.kwargs["max_tokens"] == 4096
        assert call_args.kwargs["messages"][0]["content"] == "test prompt"


def test_invoke_skill_with_custom_system_prompt():
    """Test skill invocation with custom system prompt"""
    with patch('services.anthropic_service.Anthropic') as MockAnthropic:
        mock_client = Mock()
        MockAnthropic.return_value = mock_client

        mock_response = Mock()
        mock_response.content = [Mock(text="Custom response")]
        mock_response.usage = Mock(input_tokens=15, output_tokens=25)
        mock_response.model = "claude-sonnet-4-20250514"
        mock_response.stop_reason = "end_turn"

        mock_client.messages.create.return_value = mock_response

        service = AnthropicService(api_key="test-key")
        result = service.invoke_skill(
            "test-skill",
            "test prompt",
            system_prompt="Custom system instructions",
            max_tokens=8192
        )

        assert result["success"] is True
        assert result["content"] == "Custom response"

        # Verify custom parameters were used
        call_args = mock_client.messages.create.call_args
        assert call_args.kwargs["system"] == "Custom system instructions"
        assert call_args.kwargs["max_tokens"] == 8192


@pytest.mark.asyncio
async def test_invoke_skill_streaming():
    """Test async streaming skill invocation"""
    with patch('services.anthropic_service.AsyncAnthropic') as MockAsyncAnthropic:
        mock_client = Mock()
        MockAsyncAnthropic.return_value = mock_client

        # Mock streaming context
        mock_stream = Mock()
        mock_stream.__aenter__ = AsyncMock(return_value=mock_stream)
        mock_stream.__aexit__ = AsyncMock()

        async def mock_text_stream():
            for token in ["Hello", " ", "World"]:
                yield token

        mock_stream.text_stream = mock_text_stream()

        mock_final = Mock()
        mock_final.usage = Mock(input_tokens=5, output_tokens=3)
        mock_final.model = "claude-sonnet-4-20250514"
        mock_final.stop_reason = "end_turn"
        mock_stream.get_final_message = AsyncMock(return_value=mock_final)

        mock_client.messages.stream.return_value = mock_stream

        service = AnthropicService(api_key="test-key")

        tokens = []

        async def capture_token(token):
            tokens.append(token)

        result = await service.invoke_skill_streaming(
            "test-skill",
            "test prompt",
            on_token=capture_token
        )

        assert result["success"] is True
        assert result["content"] == "Hello World"
        assert tokens == ["Hello", " ", "World"]
        assert result["usage"]["input_tokens"] == 5
        assert result["usage"]["output_tokens"] == 3
        assert result["model"] == "claude-sonnet-4-20250514"
        assert result["stop_reason"] == "end_turn"


@pytest.mark.asyncio
async def test_invoke_skill_streaming_without_callback():
    """Test streaming without on_token callback"""
    with patch('services.anthropic_service.AsyncAnthropic') as MockAsyncAnthropic:
        mock_client = Mock()
        MockAsyncAnthropic.return_value = mock_client

        mock_stream = Mock()
        mock_stream.__aenter__ = AsyncMock(return_value=mock_stream)
        mock_stream.__aexit__ = AsyncMock()

        async def mock_text_stream():
            for token in ["Test", " ", "output"]:
                yield token

        mock_stream.text_stream = mock_text_stream()

        mock_final = Mock()
        mock_final.usage = Mock(input_tokens=8, output_tokens=12)
        mock_final.model = "claude-sonnet-4-20250514"
        mock_final.stop_reason = "end_turn"
        mock_stream.get_final_message = AsyncMock(return_value=mock_final)

        mock_client.messages.stream.return_value = mock_stream

        service = AnthropicService(api_key="test-key")

        # Call without on_token callback
        result = await service.invoke_skill_streaming(
            "test-skill",
            "test prompt"
        )

        assert result["success"] is True
        assert result["content"] == "Test output"


def test_service_uses_environment_variable():
    """Test that service uses ANTHROPIC_API_KEY from environment"""
    with patch('services.anthropic_service.Anthropic') as MockAnthropic, \
         patch('services.anthropic_service.AsyncAnthropic') as MockAsyncAnthropic, \
         patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'env-key'}):

        service = AnthropicService()
        assert service.api_key == 'env-key'


def test_service_prefers_explicit_api_key():
    """Test that explicit API key overrides environment variable"""
    with patch('services.anthropic_service.Anthropic') as MockAnthropic, \
         patch('services.anthropic_service.AsyncAnthropic') as MockAsyncAnthropic, \
         patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'env-key'}):

        service = AnthropicService(api_key='explicit-key')
        assert service.api_key == 'explicit-key'


@pytest.mark.asyncio
async def test_invoke_skill_streaming_with_custom_params():
    """Test streaming with custom system prompt and max_tokens"""
    with patch('services.anthropic_service.AsyncAnthropic') as MockAsyncAnthropic:
        mock_client = Mock()
        MockAsyncAnthropic.return_value = mock_client

        mock_stream = Mock()
        mock_stream.__aenter__ = AsyncMock(return_value=mock_stream)
        mock_stream.__aexit__ = AsyncMock()

        async def mock_text_stream():
            yield "Response"

        mock_stream.text_stream = mock_text_stream()

        mock_final = Mock()
        mock_final.usage = Mock(input_tokens=20, output_tokens=30)
        mock_final.model = "claude-sonnet-4-20250514"
        mock_final.stop_reason = "max_tokens"
        mock_stream.get_final_message = AsyncMock(return_value=mock_final)

        mock_client.messages.stream.return_value = mock_stream

        service = AnthropicService(api_key="test-key")

        result = await service.invoke_skill_streaming(
            "test-skill",
            "test prompt",
            system_prompt="Custom streaming instructions",
            max_tokens=2048
        )

        assert result["success"] is True
        assert result["stop_reason"] == "max_tokens"

        # Verify parameters were passed correctly
        call_args = mock_client.messages.stream.call_args
        assert call_args.kwargs["system"] == "Custom streaming instructions"
        assert call_args.kwargs["max_tokens"] == 2048
