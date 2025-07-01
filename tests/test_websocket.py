import asyncio

from starlette.testclient import TestClient

from pyquerytracker.api import app
from pyquerytracker.websocket import (broadcast, connected_clients,
                                      websocket_endpoint)


def test_websocket_connection():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        websocket.send_text("ping")  # No response expected, just test it works


def test_broadcast_message_format():
    class FakeWebSocket:
        def __init__(self):
            self.sent = []

        async def send_text(self, msg):
            self.sent.append(msg)

    fake_ws = FakeWebSocket()
    connected_clients.append(fake_ws)

    asyncio.run(broadcast("hello"))
    assert fake_ws.sent == ["hello"]

    connected_clients.remove(fake_ws)


def test_connection_lifecycle():
    class DummyWebSocket:
        def __init__(self):
            self.accepted = False

        async def accept(self):
            self.accepted = True

        async def receive_text(self):
            raise Exception("Simulated disconnect")

    ws = DummyWebSocket()
    connected_clients.clear()
    try:
        asyncio.run(websocket_endpoint(ws))
    except Exception:
        pass
    assert ws not in connected_clients


def test_broadcast_no_clients():
    connected_clients.clear()
    try:
        asyncio.run(broadcast("no one here"))
    except Exception:
        assert False, "Broadcast failed when no clients connected"
