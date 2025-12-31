from models import Media
from sqlalchemy import LargeBinary, select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_media(session: AsyncSession, file_name: str, file_body: LargeBinary):
    new_media = Media(file_body=file_body, file_name=file_name)
    async with session.begin():
        session.add(new_media)
        await session.commit()

    return new_media


async def get_media_by_id(session: AsyncSession, media_id: int):

    async with session.begin():
        media = await session.execute(select(Media).where(Media.id == media_id))

        media_ = media.fetchone()
        if media_ is not None:

            return media_[0]
