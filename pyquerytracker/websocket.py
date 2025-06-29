from typing import List

from fastapi import WebSocket, WebSocketDisconnect

connected_clients: List[WebSocket] = []


async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        await websocket.receive_text()
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
