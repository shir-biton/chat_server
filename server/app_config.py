import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_port: int = 5432
    db_password: str = "postgres"
    db_user: str = "postgres"
    db_name: str = "chat_db"
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_url: str = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


settings = Settings()
