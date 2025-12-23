

users_data = [
    {"name": "sergey"},
    {"name": "pavel"},
    {"name": "maxim"},
    {"name": "oleg"},
    {"name": "aleksey"},
]

tweet_data = [
    {
        "tweet_data": "tweet_1",
        "author_id": 1,
        "tweet_media_ids": [1],
    },
    {
        "tweet_data": "tweet_2",
        "author_id": 1,
        "tweet_media_ids": [2, 4, 3],
    },
]

like_data = [
    {"tweets_id": 1, "name": "maxim", "id_in_users": 3},
    {"tweets_id": 2, "name": "pavel", "id_in_users": 2},
    {"tweets_id": 2, "name": "aleksey", "id_in_users": 5},
]

followed_data = [
    {"users_id": 2, "name": "maxim", "id_in_users": 3},
    {"users_id": 1, "name": "oleg", "id_in_users": 4},
    {"users_id": 3, "name": "aleksey", "id_in_users": 5},
]

image_data = [
    {"tweet_id": 1, "file_name": "cat-animals-photography.webp"},
    {"tweet_id": 2, "file_name": "sight-cat-cats.webp"},
    {"tweet_id": 2, "file_name": "cat-animals-photography.webp"},
    {"tweet_id": 2, "file_name": "item-cat-forest.webp"},
]
