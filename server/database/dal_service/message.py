from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from database.models import Message


class MessageDAL:
    @staticmethod
    async def get_messages(room: str, db: AsyncSession) -> List[Message]:
        query = (
            select(Message).where(Message.room == room)
        )
        messages = await db.stream_scalars(query)
        return [message async for message in messages]

    @staticmethod
    async def create_message(message: Message, db: AsyncSession) -> Message:
        new_message = Message(**message.model_dump())
        db.add(new_message)
        await db.commit()
        await db.refresh(new_message)
        return new_message
