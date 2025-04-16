import asyncio
import aiohttp
import json
import os


class APISession:
    def __init__(self, base_url, access_token=None):
        self.base_url = base_url
        self.access_token = access_token
        self.session = aiohttp.ClientSession()

    async def get_access_token(self, username, password):
        """POST /login"""
        url = f"{self.base_url}/login"
        json_data = {"username": username, "password": password}
        headers = {"Content-Type": "application/json"}
        async with self.session.post(url, json=json_data, headers=headers) as response:
            response_data = await response.json()
            self.access_token = response_data.get("access_token")
            return self.access_token

    async def authors_get(self):
        """GET /authors"""
        url = f"{self.base_url}/authors"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with self.session.get(url, headers=headers) as response:
            return await response.json()

    async def author_post(self, json_data):
        """POST /authors"""
        url = f"{self.base_url}/authors"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        async with self.session.post(url, json=json_data, headers=headers) as response:
            return await response.json()

    async def author_put(self, author_id, json_data):
        """PUT /authors/<id>"""
        url = f"{self.base_url}/authors/{author_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        async with self.session.put(url, json=json_data, headers=headers) as response:
            return await response.json()

    async def author_delete(self, author_id):
        """DELETE /authors/<id>"""
        url = f"{self.base_url}/authors/{author_id}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with self.session.delete(url, headers=headers) as response:
            return await response.json()

    async def books_get(self):
        """GET /books"""
        url = f"{self.base_url}/books"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with self.session.get(url, headers=headers) as response:
            return await response.json()

    async def book_get(self, book_id):
        """GET /books/<id>"""
        url = f"{self.base_url}/books/{book_id}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with self.session.get(url, headers=headers) as response:
            return await response.json()

    async def book_create(self, file_id, json_data):
        """POST /books/<id>"""
        url = f"{self.base_url}/books/{file_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        async with self.session.post(url, json=json_data, headers=headers) as response:
            return await response.json()

    async def book_update(self, book_id, json_data):
        """PUT /books/<id>"""
        url = f"{self.base_url}/books/{book_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        async with self.session.put(url, json=json_data, headers=headers) as response:
            return await response.json()

    async def book_delete(self, book_id):
        """DELETE /books/<id>"""
        url = f"{self.base_url}/books/{book_id}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with self.session.delete(url, headers=headers) as response:
            return await response.json()

    async def upload_file(self, file_path):
        """POST /file"""
        url = f"{self.base_url}/file"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        form = aiohttp.FormData()
        form.add_field(
            "file", open(file_path, "rb"), filename=os.path.basename(file_path)
        )
        async with self.session.post(url, data=form, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_text = await response.text()
                print(f"Error uploading file: {error_text}")

    async def download_file(self, filename, local_name):
        """GET /file/<id>"""
        url = f"{self.base_url}/file/{filename}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with self.session.get(url, headers=headers) as response:
            if response.status == 200:
                file_path = os.path.join("_download", local_name)
                with open(file_path, "wb") as f:
                    f.write(await response.read())
                return {"status": "success", "file_path": file_path}
            return {
                "status": "error",
                "message": f"Failed with status {response.status}",
            }

    async def add_author_to_book(self, book_id, author_id):
        """POST /books/<id>/authors"""
        url = f"{self.base_url}/books/{book_id}/authors"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
        payload = {"author_id": author_id}
        async with self.session.post(url, headers=headers, json=payload) as response:
            return await response.json()

    async def remove_author_from_book(self, book_id, author_id):
        """DELETE /books/<id>/authors"""
        url = f"{self.base_url}/books/{book_id}/authors"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
        payload = {"author_id": author_id}
        async with self.session.delete(url, headers=headers, json=payload) as response:
            return await response.json()

    async def categories_get(self):
        """GET /categories"""
        url = f"{self.base_url}/categories"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with self.session.get(url, headers=headers) as response:
            return await response.json()

    async def category_get(self, category_id):
        """GET /categories/<id>"""
        url = f"{self.base_url}/categories/{category_id}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with self.session.get(url, headers=headers) as response:
            return await response.json()

    async def category_post(self, json_data):
        """POST /categories"""
        url = f"{self.base_url}/categories"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        async with self.session.post(url, json=json_data, headers=headers) as response:
            return await response.json()

    async def category_put(self, category_id, json_data):
        """PUT /categories/<id>"""
        url = f"{self.base_url}/categories/{category_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        async with self.session.put(url, json=json_data, headers=headers) as response:
            return await response.json()

    async def category_delete(self, category_id):
        """DELETE /categories/<id>"""
        url = f"{self.base_url}/categories/{category_id}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        async with self.session.delete(url, headers=headers) as response:
            return await response.json()

    async def get_book_categories(self, book_id):
        """GET /books/<id>/categories"""
        url = f"{self.base_url}/books/{book_id}/categories"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
        async with self.session.get(url, headers=headers) as response:
            return await response.json()

    async def add_category_to_book(self, book_id, category_id):
        """POST /books/<id>/categories"""
        url = f"{self.base_url}/books/{book_id}/categories"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
        payload = {"category_id": category_id}
        async with self.session.post(url, headers=headers, json=payload) as response:
            return await response.json()

    async def remove_category_from_book(self, book_id, category_id):
        """DELETE /books/<id>/categories"""
        url = f"{self.base_url}/books/{book_id}/categories"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
        payload = {"category_id": category_id}
        async with self.session.delete(url, headers=headers, json=payload) as response:
            return await response.json()

    async def close(self):
        await self.session.close()


# Пример использования
async def main():
    file_path = "fixtures/1.pdf"
    cover_path = "fixtures/1.png"
    api_session = APISession("http://127.0.0.1:5000")

    access_token = await api_session.get_access_token("user1", "password1")
    assert len(access_token) == 331, "Error in `get_access_token`"

    # Книги
    books = await api_session.books_get()
    for book in books:
        await api_session.book_delete(book["id"])
    books = await api_session.books_get()
    assert books == [], "Error in `books_get`"

    # Загрузка книги
    book_dct = await api_session.upload_file(file_path)
    book_id = book_dct.get("id")
    filename_orig = book_dct.get("filename_orig")
    filename_uid = book_dct.get("filename_uid")
    assert book_dct == {
        "file_path": "uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf",
        "filename_orig": "1.pdf",
        "filename_uid": "3091401a1c74bfd441ace8d420f1e524.pdf",
        "id": "3091401a1c74bfd441ace8d420f1e524",
    }, "Error in `upload_file`"
    assert book_id == "3091401a1c74bfd441ace8d420f1e524", "Error in `upload_file`"
    assert filename_orig == "1.pdf", "Error in `upload_file`"
    assert (
        filename_uid == "3091401a1c74bfd441ace8d420f1e524.pdf"
    ), "Error in `upload_file`"

    # Создание книги
    ret = await api_session.book_create(book_id, json_data=book_dct)
    assert ret == {
        "authors": [],
        "categories": [],
        "cover_image": None,
        "description": None,
        "file_path": "uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf",
        "filename_orig": "1.pdf",
        "filename_uid": "3091401a1c74bfd441ace8d420f1e524.pdf",
        "id": "3091401a1c74bfd441ace8d420f1e524",
        "isbn": None,
        "publication_date": None,
        "publisher": None,
        "telegram_file_id": None,
        "telegram_link": None,
        "title": "3091401a1c74bfd441ace8d420f1e524",
    }, "Error in `book_create`"
    book_id = ret.get("id")
    assert book_id == "3091401a1c74bfd441ace8d420f1e524", "Error in `book_create`"

    # Список книг
    books = await api_session.books_get()
    assert books == [
        {
            "authors": [],
            "categories": [],
            "cover_image": None,
            "description": None,
            "file_path": "uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf",
            "filename_orig": "1.pdf",
            "filename_uid": "3091401a1c74bfd441ace8d420f1e524.pdf",
            "id": "3091401a1c74bfd441ace8d420f1e524",
            "isbn": None,
            "publication_date": None,
            "publisher": None,
            "telegram_file_id": None,
            "telegram_link": None,
            "title": "3091401a1c74bfd441ace8d420f1e524",
        }
    ], "Error in `books_get`"

    # Обновление книги
    ret = await api_session.book_update(book_id, json_data=dict())
    assert ret == {
        "authors": [],
        "categories": [],
        "cover_image": None,
        "description": None,
        "file_path": "uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf",
        "filename_orig": "1.pdf",
        "filename_uid": "3091401a1c74bfd441ace8d420f1e524.pdf",
        "id": "3091401a1c74bfd441ace8d420f1e524",
        "isbn": None,
        "publication_date": None,
        "publisher": None,
        "telegram_file_id": None,
        "telegram_link": None,
        "title": "3091401a1c74bfd441ace8d420f1e524",
    }, "Error in `book_update`"

    # Удаление книги
    ret = await api_session.book_delete(book_id)
    assert ret == {"message": "Book deleted"}, "Error in `book_delete`"

    # Получение книги
    ret = await api_session.book_get(book_id)
    assert ret == {"message": "Book not found"}, "Error in `book_get`"

    # Загрузка книги
    book_dct = await api_session.upload_file(file_path)
    book_id = book_dct.get("id")

    # Создание книги
    json_data = {
        "title": "Перечень актуальных тематик диссертационных исследований в области наук об образовании",
        "isbn": "ISBN 987-6-5432-2345-6",
        "publication_date": "2023",
        "publisher": "РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ",
        "description": "Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова",
    }
    book_dct.update(json_data)
    ret = await api_session.book_create(book_id, json_data=book_dct)
    assert ret == {'authors': [], 'categories': [], 'cover_image': None, 'description': 'Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова', 'file_path': 'uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf', 'filename_orig': '1.pdf', 'filename_uid': '3091401a1c74bfd441ace8d420f1e524.pdf', 'id': '3091401a1c74bfd441ace8d420f1e524', 'isbn': 'ISBN 987-6-5432-2345-6', 'publication_date': '2023', 'publisher': 'РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ', 'telegram_file_id': None, 'telegram_link': None, 'title': 'Перечень актуальных тематик диссертационных исследований в области наук об образовании'}, "Error in `book_create`"
    book_id = ret.get("id")
    assert book_id == "3091401a1c74bfd441ace8d420f1e524", "Error in `book_create`"

    # Получение книги
    ret = await api_session.book_get(book_id)
    assert ret == {'authors': [], 'categories': [], 'cover_image': None, 'description': 'Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова', 'file_path': 'uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf', 'filename_orig': '1.pdf', 'filename_uid': '3091401a1c74bfd441ace8d420f1e524.pdf', 'id': '3091401a1c74bfd441ace8d420f1e524', 'isbn': 'ISBN 987-6-5432-2345-6', 'publication_date': '2023', 'publisher': 'РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ', 'telegram_file_id': None, 'telegram_link': None, 'title': 'Перечень актуальных тематик диссертационных исследований в области наук об образовании'}, "Error in `book_get`"

    # Список книг
    books = await api_session.books_get()
    assert books == [{'authors': [], 'categories': [], 'cover_image': None, 'description': 'Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова', 'file_path': 'uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf', 'filename_orig': '1.pdf', 'filename_uid': '3091401a1c74bfd441ace8d420f1e524.pdf', 'id': '3091401a1c74bfd441ace8d420f1e524', 'isbn': 'ISBN 987-6-5432-2345-6', 'publication_date': '2023', 'publisher': 'РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ', 'telegram_file_id': None, 'telegram_link': None, 'title': 'Перечень актуальных тематик диссертационных исследований в области наук об образовании'}], "Error in `books_get`"

    # Обновление книги
    json_data = {"title": "Список тем"}
    ret = await api_session.book_update(book_id, json_data)
    assert ret == {'authors': [], 'categories': [], 'cover_image': None, 'description': 'Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова', 'file_path': 'uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf', 'filename_orig': '1.pdf', 'filename_uid': '3091401a1c74bfd441ace8d420f1e524.pdf', 'id': '3091401a1c74bfd441ace8d420f1e524', 'isbn': 'ISBN 987-6-5432-2345-6', 'publication_date': '2023', 'publisher': 'РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ', 'telegram_file_id': None, 'telegram_link': None, 'title': 'Список тем'}, "Error in `book_update`"

    json_data = {"isbn": None}
    ret = await api_session.book_update(book_id, json_data)
    assert ret == {'authors': [], 'categories': [], 'cover_image': None, 'description': 'Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова', 'file_path': 'uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf', 'filename_orig': '1.pdf', 'filename_uid': '3091401a1c74bfd441ace8d420f1e524.pdf', 'id': '3091401a1c74bfd441ace8d420f1e524', 'isbn': None, 'publication_date': '2023', 'publisher': 'РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ', 'telegram_file_id': None, 'telegram_link': None, 'title': 'Список тем'}, "Error in `book_update`"

    json_data = {"isbn": "ISBN 987-6-5432-2345-6"}
    ret = await api_session.book_update(book_id, json_data)
    assert ret == {'authors': [], 'categories': [], 'cover_image': None, 'description': 'Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова', 'file_path': 'uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf', 'filename_orig': '1.pdf', 'filename_uid': '3091401a1c74bfd441ace8d420f1e524.pdf', 'id': '3091401a1c74bfd441ace8d420f1e524', 'isbn': 'ISBN 987-6-5432-2345-6', 'publication_date': '2023', 'publisher': 'РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ', 'telegram_file_id': None, 'telegram_link': None, 'title': 'Список тем'}, "Error in `book_update`"



    ret = await api_session.book_get(book_id)
    assert ret == {'authors': [], 'categories': [], 'cover_image': None, 'description': 'Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова', 'file_path': 'uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf', 'filename_orig': '1.pdf', 'filename_uid': '3091401a1c74bfd441ace8d420f1e524.pdf', 'id': '3091401a1c74bfd441ace8d420f1e524', 'isbn': 'ISBN 987-6-5432-2345-6', 'publication_date': '2023', 'publisher': 'РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ', 'telegram_file_id': None, 'telegram_link': None, 'title': 'Список тем'}, "Error in `book_get`"

    books = await api_session.books_get()
    assert books == [{'authors': [], 'categories': [], 'cover_image': None, 'description': 'Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова', 'file_path': 'uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf', 'filename_orig': '1.pdf', 'filename_uid': '3091401a1c74bfd441ace8d420f1e524.pdf', 'id': '3091401a1c74bfd441ace8d420f1e524', 'isbn': 'ISBN 987-6-5432-2345-6', 'publication_date': '2023', 'publisher': 'РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ', 'telegram_file_id': None, 'telegram_link': None, 'title': 'Список тем'}], "Error in `books_get`"

    # Авторы
    authors = await api_session.authors_get()
    for author in authors:
        await api_session.author_delete(author["id"])
    authors = await api_session.authors_get()
    assert authors == [], "Error in `authors_get`"

    # Добавление автора
    json_data = {"name": "Ю.В. Китаев"}
    ret = await api_session.author_post(json_data)
    author_id = ret.get("id")
    assert ret == {
        "id": 1,
        "name": "Ю.В. Китаев",
        "name_eng": None,
    }, "Error in `author_post`"
    assert author_id == 1, "Error in `author_post`"

    # Обновление автора
    json_data = {"name": "Ю.В. Китаев", "name_eng": "Kitayev Yu. V."}
    ret = await api_session.author_put(author_id, json_data)
    assert ret == {
        "id": 1,
        "name": "Ю.В. Китаев",
        "name_eng": "Kitayev Yu. V.",
    }, "Error in `author_put`"

    # Добавление автора в список авторов книги
    ret = await api_session.add_author_to_book(book_id, author_id)
    assert ret == {
        "message": "Author added to the book"
    }, "Error in `add_author_to_book`"

    # Добавление автора в список авторов книги
    ret = await api_session.add_author_to_book(book_id, author_id)
    assert ret == {
        "message": "Author already added to the book"
    }, "Error in `add_author_to_book`"

    # Загрузка обложки
    ret = await api_session.upload_file(cover_path)
    assert ret == {
        "file_path": "uploads/92/6d/926d51b67bd5143a49f70513bef45952.png",
        "filename_orig": "1.png",
        "filename_uid": "926d51b67bd5143a49f70513bef45952.png",
        "id": "926d51b67bd5143a49f70513bef45952",
    }, "Error in `file_upload`"

    # Обновление обложки книги
    json_data = {"cover_image": ret["file_path"]}
    ret = await api_session.book_update(book_id, json_data)
    assert ret == {'authors': [{'id': 1, 'name': 'Ю.В. Китаев', 'name_eng': 'Kitayev Yu. V.'}], 'categories': [], 'cover_image': 'uploads/92/6d/926d51b67bd5143a49f70513bef45952.png', 'description': 'Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова', 'file_path': 'uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf', 'filename_orig': '1.pdf', 'filename_uid': '3091401a1c74bfd441ace8d420f1e524.pdf', 'id': '3091401a1c74bfd441ace8d420f1e524', 'isbn': 'ISBN 987-6-5432-2345-6', 'publication_date': '2023', 'publisher': 'РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ', 'telegram_file_id': None, 'telegram_link': None, 'title': 'Список тем'}, "Error in `book_update`"

    # Обновление обложки книги
    json_data = dict()
    ret = await api_session.book_update(book_id, json_data)
    assert ret == {'authors': [{'id': 1, 'name': 'Ю.В. Китаев', 'name_eng': 'Kitayev Yu. V.'}], 'categories': [], 'cover_image': 'uploads/92/6d/926d51b67bd5143a49f70513bef45952.png', 'description': 'Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова', 'file_path': 'uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf', 'filename_orig': '1.pdf', 'filename_uid': '3091401a1c74bfd441ace8d420f1e524.pdf', 'id': '3091401a1c74bfd441ace8d420f1e524', 'isbn': 'ISBN 987-6-5432-2345-6', 'publication_date': '2023', 'publisher': 'РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ', 'telegram_file_id': None, 'telegram_link': None, 'title': 'Список тем'}, "Error in `book_update`"

    # Загрузка книги
    ret = await api_session.book_get(book_id)
    assert ret == {'authors': [{'id': 1, 'name': 'Ю.В. Китаев', 'name_eng': 'Kitayev Yu. V.'}], 'categories': [], 'cover_image': 'uploads/92/6d/926d51b67bd5143a49f70513bef45952.png', 'description': 'Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова', 'file_path': 'uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf', 'filename_orig': '1.pdf', 'filename_uid': '3091401a1c74bfd441ace8d420f1e524.pdf', 'id': '3091401a1c74bfd441ace8d420f1e524', 'isbn': 'ISBN 987-6-5432-2345-6', 'publication_date': '2023', 'publisher': 'РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ', 'telegram_file_id': None, 'telegram_link': None, 'title': 'Список тем'}, "Error in `book_get`"

    # Добавление автора в список авторов книги
    ret = await api_session.add_author_to_book(book_id, author_id)
    assert ret == {
        "message": "Author already added to the book"
    }, "Error in `add_author_to_book`"

    # Загрузка книги
    ret = await api_session.book_get(book_id)
    assert ret == {'authors': [{'id': 1, 'name': 'Ю.В. Китаев', 'name_eng': 'Kitayev Yu. V.'}], 'categories': [], 'cover_image': 'uploads/92/6d/926d51b67bd5143a49f70513bef45952.png', 'description': 'Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова', 'file_path': 'uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf', 'filename_orig': '1.pdf', 'filename_uid': '3091401a1c74bfd441ace8d420f1e524.pdf', 'id': '3091401a1c74bfd441ace8d420f1e524', 'isbn': 'ISBN 987-6-5432-2345-6', 'publication_date': '2023', 'publisher': 'РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ', 'telegram_file_id': None, 'telegram_link': None, 'title': 'Список тем'}, "Error in `book_get`"

    # Удаление автора из списка авторов книги
    ret = await api_session.remove_author_from_book(book_id, author_id)
    assert ret == {
        "message": "Author removed to the book"
    }, "Error in `remove_author_from_book`"

    # Загрузка книги
    ret = await api_session.book_get(book_id)
    assert ret == {'authors': [], 'categories': [], 'cover_image': 'uploads/92/6d/926d51b67bd5143a49f70513bef45952.png', 'description': 'Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова', 'file_path': 'uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf', 'filename_orig': '1.pdf', 'filename_uid': '3091401a1c74bfd441ace8d420f1e524.pdf', 'id': '3091401a1c74bfd441ace8d420f1e524', 'isbn': 'ISBN 987-6-5432-2345-6', 'publication_date': '2023', 'publisher': 'РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ', 'telegram_file_id': None, 'telegram_link': None, 'title': 'Список тем'}, "Error in `book_get`"

    # Удаление автора из списка авторов книги
    ret = await api_session.remove_author_from_book(book_id, author_id)
    assert ret == {
        "message": "Author not found in the book"
    }, "Error in `remove_author_from_book`"

    # Получение всех категорий
    ret = await api_session.categories_get()
    # Удаление всех категорий
    for cat in ret:
        ret = await api_session.category_delete(cat["id"])
        assert ret == {"message": "Category deleted"}, "Error in `category_delete`"

    # Получение всех категорий
    ret = await api_session.categories_get()
    assert ret == [], "Error in `categories_get`"

    # Получение категории 1
    ret = await api_session.category_get(1)
    assert ret == {"message": "Category not found"}, "Error in `category_get`"

    # Получение категории 1
    ret = await api_session.category_delete(1)
    assert ret == {"message": "Category not found"}, "Error in `category_delete`"

    # Создание новой категории
    json_data = {"name": "Классика"}
    ret = await api_session.category_post(json_data)
    assert ret == {"id": 1, "name": "Классика"}, "Error in `category_post`"
    category_id = ret.get("id")

    # Переименование категории
    json_data = {"name": "Современная классика"}
    ret = await api_session.category_put(category_id, json_data)
    assert ret == {"id": 1, "name": "Современная классика"}, "Error in `category_put`"

    # Добавление книги в категорию
    ret = await api_session.add_category_to_book(book_id, category_id)
    assert ret == {
        "message": "Category added to the book"
    }, "Error in `add_category_to_book`"

    # Загрузка книги
    ret = await api_session.book_get(book_id)
    assert ret == {'authors': [], 'categories': [{'id': 1, 'name': 'Современная классика'}], 'cover_image': 'uploads/92/6d/926d51b67bd5143a49f70513bef45952.png', 'description': 'Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова', 'file_path': 'uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf', 'filename_orig': '1.pdf', 'filename_uid': '3091401a1c74bfd441ace8d420f1e524.pdf', 'id': '3091401a1c74bfd441ace8d420f1e524', 'isbn': 'ISBN 987-6-5432-2345-6', 'publication_date': '2023', 'publisher': 'РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ', 'telegram_file_id': None, 'telegram_link': None, 'title': 'Список тем'}, "Error in `book_get`"

    # Добавление книги в категорию
    ret = await api_session.add_category_to_book(book_id, category_id)
    assert ret == {
        "message": "Category already added to the book"
    }, "Error in `add_category_to_book`"

    # Удаление книги из категории
    ret = await api_session.remove_category_from_book(book_id, category_id)
    assert ret == {
        "message": "Category removed from the book"
    }, "Error in `remove_category_from_book`"

    ret = await api_session.remove_category_from_book(book_id, category_id)
    assert ret == {
        "message": "Category not found in the book"
    }, "Error in `remove_category_from_book`"

    # Удаление категории
    ret = await api_session.category_delete(category_id)
    assert ret == {"message": "Category deleted"}, "Error in `category_delete`"

    # Удаление категории
    ret = await api_session.category_delete(category_id)
    assert ret == {"message": "Category not found"}, "Error in `category_delete`"

    # Удаление книги из категории
    ret = await api_session.remove_category_from_book(book_id, category_id)
    assert ret == {
        "message": "Category not found"
    }, "Error in `remove_category_from_book`"

    # Загрузка книги
    ret = await api_session.book_get(book_id)
    assert ret == {'authors': [], 'categories': [], 'cover_image': 'uploads/92/6d/926d51b67bd5143a49f70513bef45952.png', 'description': 'Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова', 'file_path': 'uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf', 'filename_orig': '1.pdf', 'filename_uid': '3091401a1c74bfd441ace8d420f1e524.pdf', 'id': '3091401a1c74bfd441ace8d420f1e524', 'isbn': 'ISBN 987-6-5432-2345-6', 'publication_date': '2023', 'publisher': 'РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ', 'telegram_file_id': None, 'telegram_link': None, 'title': 'Список тем'}, "Error in `book_get`"
    filename_uid = ret.get("filename_uid")

    # Скачивание книги
    ret = await api_session.download_file(filename_uid, "1.pdf")
    assert ret == {'status': 'success', 'file_path': '_download/1.pdf'}, "Error in `download_file`"

    # Удаление книги
    ret = await api_session.book_delete(book_id)
    assert ret == {"message": "Book deleted"}, "Error in `book_delete`"

    await api_session.close()
    print("Done")


# Пример использования
if __name__ == "__main__":
    asyncio.run(main())
