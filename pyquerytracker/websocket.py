import asyncio
from typing import List

from fastapi import WebSocket, WebSocketDisconnect

from pyquerytracker.db.writer import DBWriter

connected_clients: List[WebSocket] = []


async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await asyncio.sleep(2)  # every 2 seconds
            recent_logs = DBWriter.fetch_all(minutes=5)  # or a custom method
            await websocket.send_json(recent_logs)
    except WebSocketDisconnect:
        pass
    finally:
        connected_clients.remove(websocket)


async def broadcast(message: str):
    disconnected = []
    for client in connected_clients:
        try:
            await client.send_text(message)
        except Exception:
            disconnected.append(client)
    for client in disconnected:
        connected_clients.remove(client)
