from collections import defaultdict

from fastapi import WebSocket


class WebSocketManager:
    def __init__(self):
        self.connected_clients = defaultdict(list)

    async def connect(self, websocket: WebSocket, room: str, username: str):
        await websocket.accept()
        self.connected_clients[room].append({"websocket": websocket, "username": username})

    async def disconnect(self, websocket: WebSocket, room: str):
        """
        Remove the client from the connected_clients dictionary when the connection is closed
        """
        self.connected_clients[room] = [
            client for client in self.connected_clients[room] if client["websocket"] != websocket
        ]

    async def broadcast_message(self, room: str, data: dict):
        """
        Broadcast the message to all clients in the same room
        """
        for client in self.connected_clients[room]:
            await client["websocket"].send_text(f"{data['created_at']}: {data['sender']}: {data['message']}")
