from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import create_engine
from sqlmodel import SQLModel
from sqlalchemy.orm import sessionmaker

from src.config import Config


engine = AsyncEngine(create_engine(url=Config.DATABASE_URL, echo=True))

async def init_db():
    async with engine.begin() as conn:
        from src.db.models import Movie
        await conn.run_sync(SQLModel.metadata.create_all)

async def drop_movies_table():
    from src.db.models import Movie
    async with engine.begin() as conn:
        await conn.run_sync(
            lambda sync_conn: SQLModel.metadata.tables["users"].drop(sync_conn, checkfirst=True)
        )


async def get_session():
    Session = sessionmaker(
        bind=engine,  # Chọn db để kết nối tới 
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with Session() as session:
        yield session

