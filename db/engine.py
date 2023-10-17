from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base
from settings.config import (
    BOT_DB_USERNAME,
    BOT_DB_PASSWORD,
    BOT_DB_URL,
    BOT_DB_NAME,
)

URL = f"{BOT_DB_USERNAME}:{BOT_DB_PASSWORD}@{BOT_DB_URL}:5432/{BOT_DB_NAME}"

engine = create_async_engine(
    f"postgresql+asyncpg://{URL}",
    echo=True,
)
session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
Base = declarative_base()
