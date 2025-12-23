from typing import Any, Dict, List

from sqlalchemy import Column, ForeignKey, Integer, LargeBinary, Sequence, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Sequence("user_id_seq"), primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    followers: Mapped[List["Follower"]] = relationship(
        back_populates="users", cascade="all, delete-orphan", lazy="selectin"
    )
    tweets: Mapped[List["Tweet"]] = relationship(
        back_populates="authors", cascade="all, delete-orphan", lazy="selectin"
    )

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Follower(Base):
    __tablename__ = "followers"
    id: Mapped[int] = mapped_column(Sequence("follower_id_seq"), primary_key=True)
    users_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(nullable=False)
    id_in_users: Mapped[int] = mapped_column(nullable=False)
    users: Mapped[List["User"]] = relationship(back_populates="followers")

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Tweet(Base):
    __tablename__ = "tweets"
    id: Mapped[int] = mapped_column(Sequence("tweets_id_seq"), primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    tweet_data: Mapped[str] = mapped_column(nullable=False)
    tweet_media_ids: Mapped[List[int]] = mapped_column(ARRAY(Integer), nullable=True)
    authors: Mapped[List["User"]] = relationship(back_populates="tweets")
    likes: Mapped[List["Like"]] = relationship(
        back_populates="tweets_likes", cascade="all, delete-orphan", lazy="selectin"
    )
    attachments: Mapped[List["Media"]] = relationship(
        back_populates="tweet", cascade="all, delete-orphan", lazy="selectin"
    )

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Like(Base):
    __tablename__ = "likes"
    id: Mapped[int] = mapped_column(Sequence("likes_id_seq"), primary_key=True)
    tweets_id: Mapped[int] = mapped_column(ForeignKey("tweets.id"))
    name: Mapped[str] = mapped_column(nullable=False)
    id_in_users: Mapped[int] = mapped_column(nullable=False)
    tweets_likes: Mapped[List["Tweet"]] = relationship(back_populates="likes")

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Media(Base):
    __tablename__ = "medias"

    id = Column(Integer, primary_key=True)
    file_body = Column(LargeBinary)
    file_name = Column(String)
    tweet_id = Column(Integer, ForeignKey("tweets.id"), nullable=True)
    tweet = relationship("Tweet", back_populates="attachments")
