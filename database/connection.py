from typing import Annotated, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database import CONNECTION_URL

engine = create_async_engine(
    CONNECTION_URL,
    echo=True,  # TODO: false in production
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def start_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


try:
    from fastapi import Depends

    SessionDependency = Annotated[AsyncSession, Depends(start_async_session)]
except ImportError:
    __all__ = ["AsyncSessionLocal"]
else:
    __all__ = ["SessionDependency", "AsyncSessionLocal"]
