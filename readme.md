# Сервис микроблогов

Установка и запуск через docker compose up

## Работа в Swagger FastAPI

1. Добавление USER

   URL: /api/user Method: POST

    Вводится имя пользователя


2. Добавление Tweet

   URL: /api/tweets Method: POST

    Вводится текст твита и список id картинок


3. Удаление Tweet

   URL: /api/tweets/{id} Method: DELETE

    Вводится id твита



4. Добавление Like

   URL: /api/tweets/{id}/likes Method: POST

    Вводится id твита и имя того кто поставил like


5. Удаление Like

   URL: /api/tweets/{id}/likes Method: DELETE

    Вводится id твита и имя того кто поставил like   



6. Добавление Follower

   URL: /api/users/{id}/follow Method: POST

    Вводится id followera и имя того кому подписывается этот follower


7. Удаление Follower

   URL: /api/users/{id}/follow Method: DELETE

    Вводится id followera и имя того кому подписывается этот follower


8. Получение списка твитов

   URL: /api/tweets Method: GET


9. Получение информации о себе

   URL: /api/users/me Method: GET


10. Получение информации о user по id

    URL: /api/users/{id} Method: GET


11. Создание изображения

    URL: /api/medias Method: POST

    Выбирается файл с изображением


12. Получение изображения

    URL: /api/medias/{media_id} Method: GET

    Выбирается id изображения    