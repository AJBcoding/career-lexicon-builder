from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from pathlib import Path
import os
from typing import Optional, Dict, Any
from services.chat_service import ChatService
from services.anthropic_service import AnthropicService
from services.project_service import ProjectService
from api.websocket import get_connection_manager

router = APIRouter(prefix="/api/chat", tags=["chat"])


def get_chat_service():
    anthropic_service = AnthropicService()
    return ChatService(anthropic_service)


def get_project_service():
    apps_dir = Path(os.getenv("APPLICATIONS_DIR", "./applications"))
    return ProjectService(apps_dir)


class ChatMessageRequest(BaseModel):
    project_id: str
    message: str
    context: Optional[Dict[str, Any]] = None


class ChatMessageResponse(BaseModel):
    message_id: str
    intent: Optional[Dict[str, Any]] = None
    response_type: str  # "conversational" or "skill_execution"
    streaming: bool = True


@router.post("/message", response_model=ChatMessageResponse)
async def send_message(
    request: ChatMessageRequest,
    background_tasks: BackgroundTasks,
    chat_service: ChatService = Depends(get_chat_service),
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Process a natural language message from the user.
    Classifies intent and routes to appropriate skill or conversational response.
    """
    # Get project info for context
    try:
        project = project_service.get_project(request.project_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Project not found")

    # Build context
    context = request.context or {}
    context.update({
        "institution": project.get("institution", "Unknown"),
        "position": project.get("position", "Unknown"),
        "stage": project.get("current_stage", "setup"),
        "files": []  # TODO: Get actual file list
    })

    # Classify intent first
    intent = await chat_service.classify_intent(request.message, context)

    # Generate message ID
    import uuid
    message_id = str(uuid.uuid4())

    # Execute in background with streaming
    background_tasks.add_task(
        execute_chat_message,
        chat_service,
        request.project_id,
        request.message,
        context,
        intent,
        message_id
    )

    return ChatMessageResponse(
        message_id=message_id,
        intent=intent,
        response_type="skill_execution" if intent["skill"] != "conversational" else "conversational",
        streaming=True
    )


async def execute_chat_message(
    chat_service: ChatService,
    project_id: str,
    message: str,
    context: Dict[str, Any],
    intent: Dict[str, Any],
    message_id: str
):
    """Execute chat message handling with WebSocket streaming"""
    manager = get_connection_manager()

    # Send start message
    await manager.broadcast_to_project(
        {
            "type": "chat_start",
            "message_id": message_id,
            "intent": intent,
            "project_id": project_id
        },
        project_id
    )

    async def on_token(token: str):
        """Stream tokens back to client"""
        await manager.broadcast_to_project(
            {
                "type": "chat_token",
                "message_id": message_id,
                "token": token
            },
            project_id
        )

    try:
        result = await chat_service.handle_message(
            project_id=project_id,
            message=message,
            context=context,
            on_token=on_token
        )

        # Send completion message
        await manager.broadcast_to_project(
            {
                "type": "chat_complete",
                "message_id": message_id,
                "result": {
                    "type": result["type"],
                    "intent": result["intent"]
                },
                "usage": result.get("result", {}).get("usage") if result["type"] == "skill_execution" else None
            },
            project_id
        )
    except Exception as e:
        # Send error message
        await manager.broadcast_to_project(
            {
                "type": "chat_error",
                "message_id": message_id,
                "error": str(e)
            },
            project_id
        )


@router.get("/history/{project_id}")
async def get_chat_history(project_id: str):
    """
    Get chat message history for a project.
    TODO: Implement message persistence
    """
    # For MVP, return empty history
    # In production, this would query a database
    return {"messages": []}
