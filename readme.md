
### Ресурсы для управления книгами

1. **BookList (`/books`)**
   - **Методы**: GET, POST
   - **Описание**: 
     - **GET**: Получение списка всех книг. Возвращает информацию о каждой книге, такую как идентификатор, название, авторы и категории.
     - **POST**: Добавление новой книги. Ожидает данные о книге, такие как название, идентификатор автора и категории.

2. **Book (`/books/<string:book_id>`)**
   - **Методы**: GET, PUT, DELETE
   - **Описание**: 
     - **GET**: Получение информации о конкретной книге по её идентификатору.
     - **PUT**: Обновление информации о книге. Ожидает данные, которые необходимо обновить.
     - **DELETE**: Удаление книги по её идентификатору.

### Ресурсы для управления авторами

3. **AuthorList (`/authors`)**
   - **Методы**: GET, POST
   - **Описание**: 
     - **GET**: Получение списка всех авторов.
     - **POST**: Добавление нового автора. Ожидает данные об авторе, такие как имя и другие детали.

4. **Author (`/authors/<string:author_id>`)**
   - **Методы**: GET, PUT, DELETE
   - **Описание**: 
     - **GET**: Получение информации о конкретном авторе по его идентификатору.
     - **PUT**: Обновление информации об авторе. Ожидает данные, которые необходимо обновить.
     - **DELETE**: Удаление автора по его идентификатору.

### Ресурсы для управления категориями

5. **CategoryList (`/categories`)**
   - **Методы**: GET, POST
   - **Описание**: 
     - **GET**: Получение списка всех категорий.
     - **POST**: Добавление новой категории. Ожидает данные о категории, такие как название и описание.

6. **Category (`/categories/<string:category_id>`)**
   - **Методы**: GET, PUT, DELETE
   - **Описание**: 
     - **GET**: Получение информации о конкретной категории по её идентификатору.
     - **PUT**: Обновление информации о категории. Ожидает данные, которые необходимо обновить.
     - **DELETE**: Удаление категории по её идентификатору.

### Ресурсы для загрузки и скачивания файлов

7. **FileUpload (`/upload`)**
   - **Методы**: POST
   - **Описание**: Загрузка файла на сервер. Ожидает файл в теле запроса.

8. **FileDownload (`/download/<string:book_id>`)**
   - **Методы**: GET
   - **Описание**: Скачивание файла, связанного с конкретной книгой. Возвращает файл, связанный с указанным идентификатором книги.

### Ресурсы для связи книг с авторами и категориями

9. **BookAuthors (`/books/<string:book_id>/authors`)**
   - **Методы**: GET, POST, DELETE
   - **Описание**: 
     - **GET**: Получение списка авторов, связанных с конкретной книгой.
     - **POST**: Добавление автора к книге.
     - **DELETE**: Удаление связи между автором и книгой.

10. **BookCategories (`/books/<string:book_id>/categories`)**
    - **Методы**: GET, POST, DELETE
    - **Описание**: 
      - **GET**: Получение списка категорий, связанных с конкретной книгой.
      - **POST**: Добавление категории к книге.
      - **DELETE**: Удаление связи между категорией и книгой.

