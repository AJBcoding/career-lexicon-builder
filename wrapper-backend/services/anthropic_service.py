from anthropic import Anthropic, AsyncAnthropic
from typing import Optional, Callable, Awaitable
import os


class AnthropicService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=self.api_key)
        self.async_client = AsyncAnthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"

    def invoke_skill(
        self,
        skill_name: str,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096
    ) -> dict:
        """Synchronous skill invocation via API"""
        messages = [{"role": "user", "content": prompt}]

        if not system_prompt:
            system_prompt = f"You are executing the {skill_name} skill. Follow the skill instructions precisely."

        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=messages
        )

        return {
            "success": True,
            "content": response.content[0].text,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            },
            "model": response.model,
            "stop_reason": response.stop_reason
        }

    async def invoke_skill_streaming(
        self,
        skill_name: str,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        on_token: Optional[Callable[[str], Awaitable[None]]] = None
    ) -> dict:
        """Async streaming skill invocation"""
        messages = [{"role": "user", "content": prompt}]

        if not system_prompt:
            system_prompt = f"You are executing the {skill_name} skill. Follow the skill instructions precisely."

        full_content = []

        async with self.async_client.messages.stream(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=messages
        ) as stream:
            async for text in stream.text_stream:
                full_content.append(text)
                if on_token:
                    await on_token(text)

        # Get final message for usage stats
        final_message = await stream.get_final_message()

        return {
            "success": True,
            "content": "".join(full_content),
            "usage": {
                "input_tokens": final_message.usage.input_tokens,
                "output_tokens": final_message.usage.output_tokens
            },
            "model": final_message.model,
            "stop_reason": final_message.stop_reason
        }
