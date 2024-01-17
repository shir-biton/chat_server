from fastapi import WebSocket, WebSocketDisconnect, Depends, APIRouter
from sqlmodel.ext.asyncio.session import AsyncSession

from api.websocket.ws_manager import WebSocketManager
from database import database
from database.dal_service import MessageDAL
from database.models import Message


class ChatWebSocketAPI:
    def __init__(self):
        self._init_routes()
        self.websocket_manager = WebSocketManager()
        self.message_dal = MessageDAL()

    def _init_routes(self) -> None:
        self.router = APIRouter(prefix="/ws", tags=["Websocket"])
        self.router.add_api_websocket_route("/{room}/{username}", self.websocket_endpoint)

    async def websocket_endpoint(
            self, websocket: WebSocket, room: str, username: str, db: AsyncSession = Depends(database.get_db)
    ):
        await self.websocket_manager.connect(websocket, room, username)
        try:
            while True:
                data = await websocket.receive_json()
                message: Message = Message(**data)
                new_message = await MessageDAL.create_message(message=message, db=db)
                await self.websocket_manager.broadcast_message(room, new_message.dict())
        except WebSocketDisconnect:
            await self.websocket_manager.disconnect(websocket, room)
