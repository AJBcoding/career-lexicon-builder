from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List
import json
import asyncio

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        # Map project_id to list of active connections
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, project_id: str):
        await websocket.accept()
        if project_id not in self.active_connections:
            self.active_connections[project_id] = []
        self.active_connections[project_id].append(websocket)

        # Send welcome message
        await self.send_personal_message(
            {"type": "connection", "status": "connected", "project_id": project_id},
            websocket
        )

    def disconnect(self, websocket: WebSocket, project_id: str):
        if project_id in self.active_connections:
            if websocket in self.active_connections[project_id]:
                self.active_connections[project_id].remove(websocket)
            if not self.active_connections[project_id]:
                del self.active_connections[project_id]

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast_to_project(self, message: dict, project_id: str):
        """Broadcast message to all connections for a specific project"""
        if project_id in self.active_connections:
            for connection in self.active_connections[project_id]:
                try:
                    await connection.send_json(message)
                except:
                    # Connection might be closed
                    pass

    async def broadcast_all(self, message: dict):
        """Broadcast to all connections"""
        for project_id, connections in self.active_connections.items():
            for connection in connections:
                try:
                    await connection.send_json(message)
                except:
                    pass

manager = ConnectionManager()

@router.websocket("/ws/{project_id}")
async def websocket_endpoint(websocket: WebSocket, project_id: str):
    from services.project_watcher_manager import get_project_watcher_manager

    await manager.connect(websocket, project_id)

    # Start watching project when first client connects
    watcher_manager = get_project_watcher_manager()
    await watcher_manager.start_watching_project(project_id)

    try:
        while True:
            # Receive messages from client
            data = await websocket.receive_text()
            message = json.loads(data)

            # Heartbeat/ping-pong
            if message.get("type") == "ping":
                await manager.send_personal_message(
                    {"type": "pong"},
                    websocket
                )
            else:
                # Echo back for now (can be extended for client messages)
                await manager.send_personal_message(
                    {"type": "echo", "data": message},
                    websocket
                )

    except WebSocketDisconnect:
        manager.disconnect(websocket, project_id)

        # Stop watching if no more clients for this project
        if project_id not in manager.active_connections or not manager.active_connections[project_id]:
            watcher_manager.stop_watching_project(project_id)
    except Exception as e:
        manager.disconnect(websocket, project_id)

        # Stop watching if no more clients for this project
        if project_id not in manager.active_connections or not manager.active_connections[project_id]:
            watcher_manager.stop_watching_project(project_id)

# Export manager for use in other modules
def get_connection_manager():
    return manager
