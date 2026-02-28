from fastapi import APIRouter, WebSocket
from typing import List

router = APIRouter(prefix="/ws", tags=["WebSockets"])

active_connections: List[WebSocket] = []

async def broadcast(message: str):
    for connection in active_connections:
        await connection.send_text(message)

@router.websocket("/tasks")
async def task_updates(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # keep alive
    except:
        active_connections.remove(websocket)