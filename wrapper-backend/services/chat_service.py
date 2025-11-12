from services.anthropic_service import AnthropicService
from typing import Callable, Awaitable, Optional, Dict, Any
import json
import logging

logger = logging.getLogger(__name__)

class ChatService:
    """Service for handling conversational interactions with natural language intent classification"""

    def __init__(self, anthropic_service: AnthropicService):
        self.anthropic = anthropic_service

        # Intent patterns mapped to skills
        self.intent_patterns = {
            "job-description-analysis": [
                "analyze job", "analyze the job", "analyze job description",
                "analyze posting", "analyze job posting", "review job",
                "what are the requirements", "parse job"
            ],
            "resume-alignment": [
                "align resume", "align my resume", "tailor resume",
                "adapt resume", "customize resume", "match resume",
                "create resume", "make resume"
            ],
            "cover-letter-voice": [
                "write cover letter", "draft cover letter", "create cover letter",
                "compose cover letter", "cover letter", "write letter"
            ],
            "format-resume": [
                "format resume", "format my resume", "clean up resume",
                "style resume", "polish resume"
            ],
            "format-cover-letter": [
                "format cover letter", "format my cover letter", "clean up letter",
                "style letter", "polish cover letter"
            ],
            "job-fit-analysis": [
                "analyze fit", "fit analysis", "am i qualified",
                "do i match", "check fit", "gap analysis"
            ]
        }

    async def classify_intent(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use Claude to determine user intent and appropriate skill

        Args:
            message: User's natural language message
            context: Context about current project (files, stage, etc.)

        Returns:
            Dict with skill name, confidence, and parameters
        """
        # Build context string
        context_str = f"Project: {context.get('institution', 'Unknown')} - {context.get('position', 'Unknown')}\n"
        context_str += f"Current stage: {context.get('stage', 'Unknown')}\n"
        if context.get('files'):
            context_str += f"Available files: {', '.join(context['files'])}\n"

        classification_prompt = f"""You are a conversational AI assistant helping with job application workflows.
Analyze the user's message and determine what skill/action they want to perform.

Context:
{context_str}

Available skills and their purposes:
- job-description-analysis: Analyze a job posting to extract requirements, culture, values
- resume-alignment: Tailor resume to match job requirements using verified achievements
- cover-letter-voice: Draft an authentic cover letter narrative
- format-resume: Format and polish resume document
- format-cover-letter: Format and polish cover letter document
- job-fit-analysis: Analyze fit between job requirements and candidate background

User message: "{message}"

Respond with ONLY a JSON object (no other text) with this structure:
{{
    "skill": "skill-name-here",
    "confidence": 0.95,
    "reasoning": "brief explanation",
    "parameters": {{}}
}}

If the message is unclear or conversational (like "hello", "thanks", etc), use:
{{
    "skill": "conversational",
    "confidence": 1.0,
    "reasoning": "Conversational message, not a skill request",
    "parameters": {{}}
}}"""

        try:
            # Use synchronous call for quick classification
            result = self.anthropic.client.messages.create(
                model=self.anthropic.model,
                max_tokens=500,
                temperature=0.1,  # Low temperature for consistent classification
                messages=[{"role": "user", "content": classification_prompt}]
            )

            response_text = result.content[0].text.strip()

            # Extract JSON from response (handle potential markdown code blocks)
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()

            intent = json.loads(response_text)

            logger.info("Intent classified", extra={
                'intent': intent.get('skill'),
                'confidence': intent.get('confidence', 0),
                'user_message_length': len(message),
                'reasoning': intent.get('reasoning', '')[:100]  # Truncated
            })

            return intent

        except Exception as e:
            logger.warning("Intent classification failed, using fallback", extra={
                'error': str(e),
                'error_type': type(e).__name__
            })
            # Fallback: use simple pattern matching
            return self._fallback_intent_classification(message)

    def _fallback_intent_classification(self, message: str) -> Dict[str, Any]:
        """Simple pattern matching fallback for intent classification"""
        message_lower = message.lower()

        for skill, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if pattern in message_lower:
                    return {
                        "skill": skill,
                        "confidence": 0.7,
                        "reasoning": f"Matched pattern: {pattern}",
                        "parameters": {}
                    }

        # No match - conversational
        return {
            "skill": "conversational",
            "confidence": 1.0,
            "reasoning": "No skill pattern matched",
            "parameters": {}
        }

    async def handle_message(
        self,
        project_id: str,
        message: str,
        context: Dict[str, Any],
        on_token: Optional[Callable[[str], Awaitable[None]]] = None
    ) -> Dict[str, Any]:
        """
        Process a natural language message, classify intent, and execute appropriate skill

        Args:
            project_id: ID of current project
            message: User's message
            context: Project context
            on_token: Callback for streaming tokens

        Returns:
            Dict with execution results
        """
        logger.info("Handling chat message", extra={
            'project_id': project_id,
            'message_length': len(message)
        })

        # Classify intent
        intent = await self.classify_intent(message, context)

        # If conversational, just respond conversationally
        if intent["skill"] == "conversational":
            logger.info("Handling conversational message", extra={
                'project_id': project_id
            })
            response = await self._handle_conversational(message, context, on_token)
            return {
                "intent": intent,
                "response": response,
                "type": "conversational"
            }

        # Build prompt for the skill
        logger.info("Executing skill from chat", extra={
            'project_id': project_id,
            'skill_name': intent["skill"],
            'confidence': intent.get('confidence', 0)
        })

        skill_prompt = self._build_skill_prompt(intent["skill"], message, context)

        # Execute skill with streaming
        result = await self.anthropic.invoke_skill_streaming(
            skill_name=intent["skill"],
            prompt=skill_prompt,
            max_tokens=4096,
            on_token=on_token
        )

        logger.info("Chat message handled", extra={
            'project_id': project_id,
            'skill_name': intent["skill"],
            'type': 'skill_execution'
        })

        return {
            "intent": intent,
            "result": result,
            "type": "skill_execution"
        }

    def _build_skill_prompt(self, skill_name: str, user_message: str, context: Dict[str, Any]) -> str:
        """Build an appropriate prompt for the identified skill"""

        # Base prompt includes user's original intent
        prompt = f"User request: {user_message}\n\n"

        # Add context
        prompt += f"Project: {context.get('institution', 'Unknown')} - {context.get('position', 'Unknown')}\n"
        prompt += f"Current stage: {context.get('stage', 'Unknown')}\n\n"

        # Skill-specific instructions
        if skill_name == "job-description-analysis":
            prompt += "Analyze the job posting that was uploaded and save the analysis as a structured JSON document. "
            prompt += "Extract requirements, culture, values, and technical skills."

        elif skill_name == "resume-alignment":
            prompt += "Create a resume tailored to this job posting. Use verified achievements from the lexicon. "
            prompt += "Match the job requirements identified in the job analysis."

        elif skill_name == "cover-letter-voice":
            prompt += "Draft an authentic cover letter for this position. Use the voice patterns and philosophy "
            prompt += "from the lexicon. Address the cultural requirements identified in the job analysis."

        elif skill_name == "format-resume":
            prompt += "Format and polish the resume document. Ensure professional formatting, consistent styling, "
            prompt += "and proper structure."

        elif skill_name == "format-cover-letter":
            prompt += "Format and polish the cover letter document. Ensure professional formatting and proper structure."

        elif skill_name == "job-fit-analysis":
            prompt += "Analyze the fit between the candidate's background and job requirements. "
            prompt += "Identify gaps and develop reframing strategies."

        return prompt

    async def _handle_conversational(
        self,
        message: str,
        context: Dict[str, Any],
        on_token: Optional[Callable[[str], Awaitable[None]]] = None
    ) -> str:
        """Handle conversational messages that don't map to skills"""

        system_prompt = f"""You are a helpful AI assistant for job application workflows.
Be friendly, concise, and helpful. You can:
- Answer questions about the project status
- Explain what skills are available
- Provide guidance on next steps
- Clarify what actions can be performed

Current project: {context.get('institution', 'Unknown')} - {context.get('position', 'Unknown')}
Current stage: {context.get('stage', 'Unknown')}

Available actions:
- Analyze job postings
- Align resumes to job requirements
- Draft cover letters
- Format documents
- Analyze job fit"""

        full_content = []

        async with self.anthropic.async_client.messages.stream(
            model=self.anthropic.model,
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": message}]
        ) as stream:
            async for text in stream.text_stream:
                full_content.append(text)
                if on_token:
                    await on_token(text)

        return "".join(full_content)
