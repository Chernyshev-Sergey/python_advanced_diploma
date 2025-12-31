import json
import sys
from contextlib import asynccontextmanager
from typing import Annotated, Any

import models
import schemas
import service
from database import async_session, engine, session
from fastapi import Depends, FastAPI, Request, Response, UploadFile
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield
    await session.close()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


async def get_async_session():
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(request: Request, exc: ResponseValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )


@app.post("/api/user", response_model=schemas.UserOut)
async def add_user(
    user: schemas.UserIn,
    response: Response,
    session: SessionDep
) -> models.User | str:
    new_user = models.User(**user.model_dump())

    try:
        response.headers["Api-Key"] = "tests"
        async with session.begin():
            session.add(new_user)
            await session.commit()
    except Exception:
        exc_type, exc_value, _ = sys.exc_info()
        if exc_type:
            errors = {
                "result": False,
                "error_type": exc_type.__name__,
                "error_message": str(exc_value),
            }
            return json.dumps(errors)
    return new_user


@app.post("/api/tweets", response_model=schemas.TweetOut)
async def add_tweet(
    tweet: schemas.TweetIn,
    response: Response,
    session: SessionDep,
    user_name: str = "sergey"
) -> JSONResponse | str:
    new_tweet = models.Tweet(**tweet.model_dump())
    try:
        response.headers["Api-Key"] = "tests"
        async with session.begin():
            me = await session.execute(
                select(models.User).where(models.User.name == user_name)
            )
            me_ = me.fetchone()

            if me_ is not None:
                # new_tweet = models.Tweet(content=tweet.content)
                me_[0].tweets.append(new_tweet)

                # session.add(new_tweet)
            await session.commit()
        async with session.begin():
            tweets = await session.execute(
                select(models.Tweet).where(models.Tweet.id == new_tweet.id)
            )
            tweets_ = tweets.fetchone()
            if tweets_ is not None:
                media_update = (
                    update(models.Media)
                    .where(models.Media.id.in_(tweets_[0].tweet_media_ids))
                    .values(tweet_id=new_tweet.id)
                    .execution_options(synchronize_session="fetch")
                )
                await session.execute(media_update)
            await session.commit()

    except Exception:
        exc_type, exc_value, _ = sys.exc_info()
        if exc_type:
            errors = {
                "result": False,
                "error_type": exc_type.__name__,
                "error_message": str(exc_value),
            }
            return json.dumps(errors)

    return JSONResponse(
        status_code=201,
        content={"result": True, "tweet_id": new_tweet.id},
    )


@app.delete("/api/tweets/{id}", response_model=schemas.TweetOut)
async def delete_tweet_by_id(
    id: int,
    response: Response,
    session: SessionDep,
    user_name: str = "sergey"
) -> JSONResponse | str:

    try:
        response.headers["Api-Key"] = "tests"
        async with session.begin():
            me = await session.execute(
                select(models.User).where(models.User.name == user_name)
            )

            me_ = me.fetchone()
            if me_ is not None:
                tweet = await session.execute(
                    select(models.Tweet).where(
                        models.Tweet.author_id == me_[0].id, models.Tweet.id == id
                    )
                )

                tweet_ = tweet.scalar_one_or_none()
                if tweet_ is not None:
                    await session.delete(tweet_)
        await session.commit()
    except Exception:
        exc_type, exc_value, _ = sys.exc_info()
        if exc_type:
            errors = {
                "result": False,
                "error_type": exc_type.__name__,
                "error_message": str(exc_value),
            }
            return json.dumps(errors)

    return JSONResponse(
        status_code=202,
        content={"result": True},
    )


@app.patch("/api/tweets/{id}", response_model=schemas.TweetUpdateOut)
async def update_tweet_by_id(
    id: int,
    content: schemas.TweetUpdateIn,
    response: Response,
    session: SessionDep,
    user_name: str = "sergey"
) -> JSONResponse | str:
    update_tweets = models.Tweet(**content.model_dump())

    try:
        response.headers["Api-Key"] = "tests"
        async with session.begin():
            me = await session.execute(
                select(models.User).where(models.User.name == user_name)
            )

            me_ = me.fetchone()
            if me_ is not None:
                tweet = await session.execute(
                    select(models.Tweet).where(
                        models.Tweet.author_id == me_[0].id, models.Tweet.id == id
                    )
                )

                tweet_ = tweet.fetchone()
                if tweet_ is not None:

                    if update_tweets.tweet_data:
                        update_tweets_data = update_tweets.tweet_data
                    if update_tweets.tweet_media_ids:
                        update_tweet_media_ids = update_tweets.tweet_media_ids
                    if not update_tweets.tweet_data:
                        update_tweets_data = tweet_[0].tweet_data
                    if not update_tweets.tweet_media_ids:
                        update_tweet_media_ids = tweet_[0].tweet_media_ids
                    tweet_update = (
                        update(models.Tweet)
                        .where(models.Tweet.id == tweet_[0].id)
                        .values(
                            tweet_data=update_tweets_data,
                            tweet_media_ids=update_tweet_media_ids,
                        )
                        .execution_options(synchronize_session="fetch")
                    )
                    await session.execute(tweet_update)
            await session.commit()
    except Exception:
        exc_type, exc_value, _ = sys.exc_info()
        if exc_type:
            errors = {
                "result": False,
                "error_type": exc_type.__name__,
                "error_message": str(exc_value),
            }
            return json.dumps(errors)

    return JSONResponse(
        status_code=201,
        content={"result": True},
    )


@app.post("/api/tweets/{id}/likes", response_model=schemas.LikeOut)
async def add_like(
    id: int,
    response: Response,
    session: SessionDep,
    user_name: str = "sergey"
) -> JSONResponse | str:
    # new_like = models.Like(**like.model_dump())
    try:
        response.headers["Api-Key"] = "tests"
        async with session.begin():
            tweet = await session.execute(
                select(models.Tweet).where(models.Tweet.id == id)
            )

            tweet_ = tweet.fetchone()
            if tweet_ is not None:
                liker = await session.execute(
                    select(models.User).where(models.User.name == user_name)
                )

                liker_ = liker.fetchone()
                if liker_ is not None:

                    new_like = models.Like(name=user_name, id_in_users=liker_[0].id)
                    tweet_[0].likes.append(new_like)
            await session.commit()
    except Exception:
        exc_type, exc_value, _ = sys.exc_info()
        if exc_type:
            errors = {
                "result": False,
                "error_type": exc_type.__name__,
                "error_message": str(exc_value),
            }
            return json.dumps(errors)

    return JSONResponse(
        status_code=201,
        content={"result": True},
    )


@app.delete("/api/tweets/{id}/likes", response_model=schemas.LikeOut)
async def delete_like(
    id: int,
    response: Response,
    session: SessionDep,
    user_name: str = "pavel"
) -> JSONResponse | str:
    # new_like = models.Like(**like.model_dump())
    try:
        response.headers["Api-Key"] = "tests"
        async with session.begin():
            tweet = await session.execute(
                select(models.Tweet).where(models.Tweet.id == id)
            )

            tweet_ = tweet.fetchone()
            if tweet_ is not None:

                like = await session.execute(
                    select(models.Like).where(
                        models.Like.tweets_id == tweet_[0].id, models.Like.name == user_name
                    )
                )

                like_ = like.scalar_one_or_none()
                if like_ is not None:

                    await session.delete(like_)
            await session.commit()
    except Exception:
        exc_type, exc_value, _ = sys.exc_info()
        if exc_type:
            errors = {
                "result": False,
                "error_type": exc_type.__name__,
                "error_message": str(exc_value),
            }
            return json.dumps(errors)

    return JSONResponse(
        status_code=202,
        content={"result": True},
    )


@app.post("/api/users/{id}/follow", response_model=schemas.FollowerOut)
async def add_follow(
    id: int,
    response: Response,
    session: SessionDep,
    user_name: str = "oleg"
) -> JSONResponse | str:
    # new_follow = models.Follower(**follow.model_dump())
    try:
        response.headers["Api-Key"] = "tests"
        async with session.begin():
            me = await session.execute(
                select(models.User).where(models.User.name == user_name)
            )

            me_ = me.fetchone()
            if me_ is not None:
                follower = await session.execute(
                    select(models.User).where(models.User.id == id)
                )

                follower_ = follower.fetchone()
                if follower_ is not None:

                    new_follow = models.Follower(
                        name=follower_[0].name, id_in_users=follower_[0].id
                    )
                    me_[0].followers.append(new_follow)
                    # session.add(new_tweet)
            await session.commit()
    except Exception:
        exc_type, exc_value, _ = sys.exc_info()
        if exc_type:
            errors = {
                "result": False,
                "error_type": exc_type.__name__,
                "error_message": str(exc_value),
            }
            return json.dumps(errors)

    return JSONResponse(
        status_code=201,
        content={"result": True},
    )


@app.delete("/api/users/{id}/follow", response_model=schemas.FollowerOut)
async def delete_follow(
    id: int,
    response: Response,
    session: SessionDep,
    user_name: str = "sergey"
) -> JSONResponse | str:

    try:
        response.headers["Api-Key"] = "tests"
        async with session.begin():
            me = await session.execute(
                select(models.User).where(models.User.name == user_name)
            )
            me_ = me.fetchone()
            if me_ is not None:

                follow = await session.execute(
                    select(models.Follower).where(
                        models.Follower.users_id == me_[0].id,
                        models.Follower.id_in_users == id,
                    )
                )

                follow_ = follow.scalar_one_or_none()
                if follow_ is not None:
                    await session.delete(follow_)
            await session.commit()
    except Exception:
        exc_type, exc_value, _ = sys.exc_info()
        if exc_type:
            errors = {
                "result": False,
                "error_type": exc_type.__name__,
                "error_message": str(exc_value),
            }
            return json.dumps(errors)

    return JSONResponse(
        status_code=202,
        content={"result": True},
    )


@app.get("/api/tweets", response_model=schemas.TweetOut)
async def get_tweets(
    response: Response,
    session: SessionDep,
    user_name: str = "sergey"
) -> JSONResponse | str:
    tweets_list: list[Any] = []
    # new_tweet = models.Tweet(**tweet.model_dump())
    try:
        response.headers["Api-Key"] = "tests"
        async with session.begin():
            me = await session.execute(
                select(models.User).where(models.User.name == user_name)
            )

            me_ = me.fetchone()
            if me_ is not None:

                tweets = await session.execute(
                    select(models.Tweet).where(models.Tweet.author_id == me_[0].id)
                )
                tweets_ = tweets.fetchall()
                if tweets_ is not None:

                    tweets_list = []
                    attachments_list = []
                    likes_list = []
                    for tweet in tweets_:
                        for like in tweet[0].likes:
                            likes_list.append({"user_id": like.id_in_users, "name": like.name})
                        for attachment in tweet[0].tweet_media_ids:
                            attachments_list.append(f"/api/medias/{attachment}")
                        tweets_list.append(
                            {
                                "id": tweet[0].id,
                                "content": tweet[0].tweet_data,
                                "attachments": attachments_list,
                                "author": {"id": me_[0].id, "name": me_[0].name},
                                "likes": likes_list,
                            }
                        )
                        attachments_list = []
                        likes_list = []
    except Exception:
        exc_type, exc_value, _ = sys.exc_info()
        if exc_type:
            errors = {
                "result": False,
                "error_type": exc_type.__name__,
                "error_message": str(exc_value),
            }
            return json.dumps(errors)

    return JSONResponse(
        status_code=200,
        content={"result": True, "tweets": tweets_list},
    )


@app.get("/api/users/me", response_model=schemas.FollowerOut)
async def get_me(
    response: Response,
    session: SessionDep,
    user_name: str = "sergey"
) -> JSONResponse | str:
    # new_follow = models.Follower(**follow.model_dump())
    user = {}
    followers_list = []
    followings_list = []
    try:
        response.headers["Api-Key"] = "tests"
        async with session.begin():
            me = await session.execute(
                select(models.User).where(models.User.name == user_name)
            )
            me_ = me.fetchone()
            if me_ is not None:
                user_id = me_[0].id
                user_name = me_[0].name

                followers = await session.execute(
                    select(models.Follower).where(models.Follower.users_id == me_[0].id)
                )

                followers_ = followers.fetchall()
                if followers_ is not None:

                    for follower in followers_:
                        followers_list.append(
                            {"id": follower[0].id_in_users, "name": follower[0].name}
                        )

                followings = await session.execute(
                    select(models.Follower).where(models.Follower.name == me_[0].name)
                )

                followings_ = followings.fetchall()
                if followings_ is not None:
                    for following_user_ in followings_:

                        following_user = await session.execute(
                            select(models.User).where(
                                models.User.id == following_user_[0].users_id
                            )
                        )
                        follow_user = following_user.fetchone()
                        if follow_user is not None:
                            followings_list.append(
                                {
                                    "id": follow_user[0].id,
                                    "name": follow_user[0].name,
                                }
                            )
        user = {
            "id": user_id,
            "name": user_name,
            "followers": followers_list,
            "following": followings_list,
        }

    except Exception:
        exc_type, exc_value, _ = sys.exc_info()
        if exc_type:
            errors = {
                "result": False,
                "error_type": exc_type.__name__,
                "error_message": str(exc_value),
            }
            return json.dumps(errors)

    return JSONResponse(
        status_code=200,
        content={"result": True, "user": user},
    )


@app.get("/api/users/{id}", response_model=schemas.FollowerOut)
async def get_user_by_id(
    id: int, response: Response, session: SessionDep
) -> JSONResponse | str:
    result = {}
    followers_list = []
    followings_list = []
    try:
        response.headers["Api-Key"] = "tests"
        async with session.begin():
            user = await session.execute(
                select(models.User).where(models.User.id == id)
            )

            user_ = user.fetchone()
            if user_ is not None:
                user_id = user_[0].id
                user_name = user_[0].name

                followers = await session.execute(
                    select(models.Follower).where(models.Follower.users_id == user_[0].id)
                )
                followers_ = followers.fetchall()
                if followers_ is not None:
                    for follower in followers_:
                        followers_list.append(
                            {"id": follower[0].id_in_users, "name": follower[0].name}
                        )

                followings = await session.execute(
                    select(models.Follower).where(models.Follower.name == user_[0].name)
                )

                followings_ = followings.fetchall()
                if followings_ is not None:
                    for following_user_ in followings_:

                        following_user = await session.execute(
                                select(models.User).where(
                                    models.User.id == following_user_[0].users_id
                                )
                            )
                        follow_user = following_user.fetchone()
                        if follow_user is not None:

                            followings_list.append(
                                {
                                    "id": follow_user[0].id,
                                    "name": follow_user[0].name,
                                }
                            )
        result = {
            "id": user_id,
            "name": user_name,
            "followers": followers_list,
            "following": followings_list,
        }

    except Exception:
        exc_type, exc_value, _ = sys.exc_info()
        if exc_type:
            errors = {
                "result": False,
                "error_type": exc_type.__name__,
                "error_message": str(exc_value),
            }
            return json.dumps(errors)
    return JSONResponse(
        status_code=200,
        content={"result": True, "user": result},
    )



@app.post(
    "/api/medias",
    response_model=schemas.MediaOut,
    responses={404: {"model": schemas.ErrorOut}},
)
async def create_media(
    file: UploadFile, session: SessionDep
):

    file_body = await file.read()
    try:
        media = await service.create_media(  # тут описываете логику создания картинки
            session, file_name=file.filename, file_body=file_body    # type: ignore[arg-type]
        )

    except Exception:
        exc_type, exc_value, _ = sys.exc_info()
        if exc_type:
            errors = {
                "result": False,
                "error_type": exc_type.__name__,
                "error_message": str(exc_value),
            }
            return json.dumps(errors)

    return JSONResponse(
        status_code=201,
        content={"result": True, "media_id": media.id},
    )


@app.get(
    "/api/medias/{media_id}",
    response_class=Response,
    responses={404: {"model": schemas.ErrorOut}},
    response_model=None,
)
async def get_media(
    media_id: int, session: SessionDep
) -> Response | str:

    try:
        media = await service.get_media_by_id(session, media_id)
    except Exception:
        exc_type, exc_value, _ = sys.exc_info()
        if exc_type:
            errors = {
                "result": False,
                "error_type": exc_type.__name__,
                "error_message": str(exc_value),
            }
            return json.dumps(errors)

    if not media:
        error = {"result": False, "message": "Media not found"}
        return json.dumps(error)

    return Response(content=media.file_body, media_type="image/webp")
