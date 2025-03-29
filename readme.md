API Endpoints

    Книги:
        GET /books - получить список всех книг.
        GET /books/<id> - получить информацию о книге по ID.
        PUT /books/<id> - обновить информацию о книге.
        DELETE /books/<id> - удалить книгу и PDF файл.

    Авторы:
        GET /authors - получить список всех авторов.
        POST /authors - добавить нового автора.
        GET /authors/<id> - получить информацию об авторе по ID.
        PUT /authors/<id> - обновить информацию об авторе.
        DELETE /authors/<id> - удалить автора.

    Категории:
        GET /categories - получить список всех категорий.
        POST /categories - добавить новую категорию.
        GET /categories/<id> - получить информацию о категории по ID.
        PUT /categories/<id> - обновить информацию о категории.
        DELETE /categories/<id> - удалить категорию.

    Загрузка файлов:
        GET /download/<id> - скачать PDF-файл книги.
        POST /upload - загрузить PDF-файл книги и добавить новую книгу.

    Получение авторов книги: GET /books/<book_id>/authors
    Добавление автора к книге: POST /books/<book_id>/authors с JSON-телом {"author_id": "author_id"}
    Удаление автора из книги: DELETE /books/<book_id>/authors с JSON-телом {"author_id": "author_id"}
    Получение категорий книги: GET /books/<book_id>/categories
    Добавление категории к книге: POST /books/<book_id>/categories с JSON-телом {"category_id": "category_id"}
    Удаление категории из книги: DELETE /books/<book_id>/categories с JSON-телом {"category_id": "category_id"}


Интеграция с Google Books API

Для автоматического получения информации о книге используется Google Books API. 

Telegram-бот

Бот позволяет добавлять новые книги в библиотеку и публиковать информацию о них в Telegram-канал.

Логирование и обработка ошибок

Ошибки и информационные сообщения записываются в .log файл.