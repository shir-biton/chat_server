from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from server.database import database
from server.database.dal_service import MessageDAL
from server.database.models.message import Message


class ChatAPI:
    def __init__(self):
        self._init_routes()
        self.message_dal = MessageDAL()

    def _init_routes(self) -> None:
        self.router = APIRouter(prefix="/message", tags=["Messages"])
        self.router.add_api_route("/", self.create_message, methods=["POST"], response_model=Message)
        self.router.add_api_route("/{username}", self.list_messages, methods=["GET"], response_model=List[Message])

    async def create_message(
            self, message: Message, db: AsyncSession = Depends(database.get_db)
    ) -> Message:
        new_message = await self.message_dal.create_message(message=message, db=db)
        return new_message

    async def list_messages(self, username: str, db: AsyncSession = Depends(database.get_db)) -> List[Message]:
        messages = await self.message_dal.get_messages(username=username, db=db)
        return messages
