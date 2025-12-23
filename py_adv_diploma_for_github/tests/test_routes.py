# import json
# import os
# from pathlib import Path
#
# import chardet
import pytest
# from fastapi import UploadFile
from httpx import AsyncClient

# @pytest.mark.asyncio
# async def test_main_route(async_client: AsyncClient) -> None:
#     response = await async_client.get("http://0.0.0.0")
#     assert response.status_code == 200


@pytest.mark.asyncio
async def test_add_user(async_client: AsyncClient) -> None:
    new_user = {"name": "slava"}
    response = await async_client.post(
        "/api/user",
        headers={
            "Api-Key": "tests",
        },
        json=new_user,
    )
    assert response.json() == {"id": 6, "name": "slava"}
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_add_tweet(async_client: AsyncClient) -> None:
    new_tweet = {
        "tweet_data": "tweet_3",
        "tweet_media_ids": [2],
    }
    response = await async_client.post(
        "/api/tweets",
        headers={
            "Api-Key": "tests",
        },
        json=new_tweet,
    )
    assert response.json() == {"result": True, "tweet_id": 3}
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_delete_tweet_by_id(async_client: AsyncClient) -> None:
    response = await async_client.delete(
        "/api/tweets/2",
        headers={
            "Api-Key": "tests",
        },
    )
    assert response.status_code == 202


@pytest.mark.asyncio
async def test_update_tweet_by_id(async_client: AsyncClient) -> None:
    content = {"tweet_data": "check", "tweet_media_ids": [1, 2]}

    response = await async_client.patch(
        "/api/tweets/1",
        headers={
            "Api-Key": "tests",
        },
        json=content,
    )
    assert response.json() == {"result": True}
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_add_like(async_client: AsyncClient) -> None:
    new_like = {"name": "oleg"}
    response = await async_client.post(
        "/api/tweets/1/likes",
        headers={
            "Api-Key": "tests",
        },
        json=new_like,
    )
    print(response.json())
    assert response.json() == {"result": True}
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_delete_like_tweet_by_id(async_client: AsyncClient) -> None:
    response = await async_client.delete(
        "/api/tweets/2/likes",
        headers={
            "Api-Key": "tests",
        },
    )
    print(response.json())
    assert response.json() == {"result": True}
    assert response.status_code == 202


@pytest.mark.asyncio
async def test_add_follow(async_client: AsyncClient) -> None:
    new_follow = {"name": "oleg"}
    response = await async_client.post(
        "/api/users/2/follow",
        headers={
            "Api-Key": "tests",
        },
        json=new_follow,
    )
    print(response.json())
    assert response.json() == {"result": True}
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_delete_follow(async_client: AsyncClient) -> None:
    response = await async_client.delete(
        "/api/users/4/follow",
        headers={
            "Api-Key": "tests",
        },
    )
    print(response.json())
    assert response.json() == {"result": True}
    assert response.status_code == 202


@pytest.mark.asyncio
async def test_get_tweets(async_client: AsyncClient) -> None:

    response = await async_client.get(
        "/api/tweets",
        headers={
            "Api-Key": "tests",
        },
    )
    print(response.json())
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_me(async_client: AsyncClient) -> None:

    response = await async_client.get(
        "/api/users/me",
        headers={
            "Api-Key": "tests",
        },
    )
    print(response.json())
    # assert response.json() == {'result': True}
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_user_by_id(async_client: AsyncClient) -> None:

    response = await async_client.get(
        "/api/users/1",
        headers={
            "Api-Key": "tests",
        },
    )
    print(response.json())
    # assert response.json() == {'result': True}
    assert response.status_code == 200


# @pytest.mark.asyncio
# async def test_add_media(async_client: AsyncClient) -> None:
#
#     with open(os.path.abspath("tests/media/cat_1.png"), "rb") as file:
#         encoding = chardet.detect(file.read())['encoding']
#         print(encoding)
#
#     with open(os.path.abspath("tests/media/cat_1.png"), "r", encoding=encoding) as file:
#         content = file.read()
#     response = await async_client.post('/api/medias',
#                                        headers={"Api-Key": "tests", },
#                                        files={"file": content})
#     print(response.json())
#     assert response.status_code == 201
