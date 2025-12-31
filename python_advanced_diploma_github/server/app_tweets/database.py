from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql+asyncpg://tweets_db:admin@postgres_container:5432/tweets_db"
# DATABASE_URL = "postgresql+asyncpg://tweets_db:admin@localhost:5432/tweets_db"

engine = create_async_engine(DATABASE_URL, echo=True)
# expire_on_commit=False will prevent attributes from being expired
# after commit.
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
session = async_session()
Base = declarative_base()
