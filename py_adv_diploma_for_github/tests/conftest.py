from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool, insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ..server.app_tweets.config import settings
from ..server.app_tweets.database import Base
from ..server.app_tweets.models import Follower, Like, Tweet, User, Media
from ..server.app_tweets.routers import app
from ..tests import data_for_tests

test_engine = create_async_engine(str(settings.db.url), poolclass=NullPool, echo=True)
test_async_session = async_sessionmaker(bind=test_engine, expire_on_commit=False)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(autouse=True, scope="session")
async def prepare_database():
    async with test_engine.begin() as conn:

        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        await conn.execute(insert(User), data_for_tests.users_data)
        await conn.execute(insert(Follower), data_for_tests.followed_data)
        await conn.execute(insert(Tweet), data_for_tests.tweet_data)
        await conn.execute(insert(Like), data_for_tests.like_data)
        await conn.execute(insert(Media), data_for_tests.image_data)

        await conn.commit()

    yield

    # async with test_engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as async_test_client:
        yield async_test_client
