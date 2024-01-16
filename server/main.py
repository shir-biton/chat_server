import uvicorn
from fastapi import FastAPI

from api import ChatAPI
from database import database

app = FastAPI()


async def init_routes() -> None:
    app.include_router(ChatAPI().router)


@app.on_event("startup")
async def init_app() -> None:
    await database.init_db()
    await init_routes()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
