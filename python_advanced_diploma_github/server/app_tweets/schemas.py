from typing import List, Optional

from fastapi import UploadFile
from pydantic import BaseModel


class User(BaseModel):
    name: str


class UserIn(User): ...


class UserOut(User):
    id: int

    class Config:
        from_attributes = True


class Tweet(BaseModel):
    tweet_data: str
    tweet_media_ids: Optional[List[int]] = None


class TweetUpdate(BaseModel):
    tweet_data: Optional[str] = None
    tweet_media_ids: Optional[List[int]] = None


class TweetUpdateIn(TweetUpdate): ...


class TweetUpdateOut(TweetUpdate):
    id: int
    tweet_data: str
    tweet_media_ids: List[int]

    class Config:
        from_attributes = True


class TweetIn(Tweet): ...


class TweetOut(Tweet):
    id: int
    tweet_data: str
    tweet_media_ids: Optional[List[int]] = None

    class Config:
        from_attributes = True


class Like(BaseModel):
    name: str


class LikeIn(Like): ...


class LikeOut(Like):
    id: int
    name: str

    class Config:
        from_attributes = True


class Follower(BaseModel): ...


class FollowerIn(Follower): ...


class FollowerOut(Follower):
    id: int
    name: str

    class Config:
        from_attributes = True


class Attachment(BaseModel):
    attachments: Optional[str] = None


class AttachmentIn(Attachment): ...


class AttachmentOut(Attachment):
    id: int
    attachments: Optional[str] = None

    class Config:
        from_attributes = True


class TweetMedia(BaseModel):
    file: UploadFile


class TweetMediaIn(TweetMedia): ...


class TweetMediaOut(TweetMedia):
    id: int

    class Config:
        from_attributes = True


class ErrorOut(BaseModel):
    status: int = 404
    reason: str = "Error"
    details: str | None = None


class MediaIn(BaseModel):
    file: UploadFile


class MediaOut(MediaIn):
    media_id: int

    class Config:
        from_attributes = True
