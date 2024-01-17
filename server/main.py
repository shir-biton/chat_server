import logging

import uvicorn
from fastapi import FastAPI

from api import ChatAPI, ChatWebSocketAPI
from database import database

app = FastAPI()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


async def init_routes() -> None:
    app.include_router(ChatAPI().router)
    app.include_router(ChatWebSocketAPI().router)


@app.on_event("startup")
async def init_app() -> None:
    await database.init_db()
    await init_routes()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
