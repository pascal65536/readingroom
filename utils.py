import requests
import json
import os


def get_access_token(username, password, govdatahub="localhost:5000"):
    """
    POST /login
    """
    url = f"http://{govdatahub}/login"
    json_data = {"username": username, "password": password}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=json_data, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error in `get_access_token` {e}")


def get_book_authors(book_id, access_token, govdatahub="localhost:5000"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    url = f"http://{govdatahub}/books/{book_id}/authors"
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response
    except Exception as e:
        print(f"Error in `add_author_to_book` {e}")


def add_author_to_book(book_id, author_id, access_token, govdatahub="localhost:5000"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    url = f"http://{govdatahub}/books/{book_id}/authors"
    payload = {"author_id": author_id}
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.json()
    except Exception as e:
        print(f"Error in `add_author_to_book` {e}")


def remove_author_from_book(
    book_id, author_id, access_token, govdatahub="localhost:5000"
):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    url = f"http://{govdatahub}/books/{book_id}/authors"
    payload = {"author_id": author_id}
    try:
        response = requests.delete(url, headers=headers, json=payload)
        return response.json()
    except Exception as e:
        print(f"Error in `add_author_to_book` {e}")


def get_book_categories(book_id, access_token, govdatahub="localhost:5000"):
    """
    GET /books/<book_id>/categories
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"http://{govdatahub}/books/{book_id}/categories"
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error in `get_book_categories`: {e}")


def book_create(file_id, json_data, access_token, govdatahub="localhost:5000"):
    """POST /books/<id>"""
    url = f"http://{govdatahub}/books/{file_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(url, json=json_data, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error in `book_create`: {e}")


def add_category_to_book(
    book_id, category_id, access_token, govdatahub="localhost:5000"
):
    """
    POST /books/<book_id>/categories
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"http://{govdatahub}/books/{book_id}/categories"
    payload = {"category_id": category_id}
    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error in `add_category_to_book`: {e}")


def remove_category_from_book(
    book_id, category_id, access_token, govdatahub="localhost:5000"
):
    """
    DELETE /books/<book_id>/categories
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"http://{govdatahub}/books/{book_id}/categories"
    payload = {"category_id": category_id}
    try:
        response = requests.delete(url, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error in `remove_category_from_book`: {e}")


def book_get(book_id, access_token, govdatahub="localhost:5000"):
    """
    GET /books/<id>
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"http://{govdatahub}/books/{book_id}"
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error in `book_get` {e}")


def book_update(book_id, json_data, access_token, govdatahub="localhost:5000"):
    """
    PUT /books/<id>
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"http://{govdatahub}/books/{book_id}"
    try:
        response = requests.put(url, json=json_data, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error in `book_update` without cover_image: {e}")


def book_download(book_id, access_token, govdatahub="localhost:5000"):
    """
    GET /download/<id>
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"http://{govdatahub}/download/{book_id}"
    try:
        response = requests.get(url, headers=headers)
        return response
    except Exception as e:
        print(f"Error in `book_download` {e}")


def book_delete(book_id, access_token, govdatahub="localhost:5000"):
    """
    DELETE /books/<id>
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"http://{govdatahub}/books/{book_id}"
    try:
        response = requests.delete(url, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error in `book_delete` {e}")


def upload_file(file_path, access_token, govdatahub="localhost:5000"):
    """
    POST /file
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"http://{govdatahub}/file"
    json_data = {"title": file_path.split("/")[-1]}
    with open(file_path, "rb") as f:
        files = {"file": f}
        data = {"json_data": json.dumps(json_data)}
        try:
            response = requests.post(url, files=files, data=data, headers=headers)
            return response.json()
        except Exception as e:
            print(f"Error in `book_upload` {e}")


def books_get(access_token, govdatahub="localhost:5000"):
    """
    GET /books
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"http://{govdatahub}/books"
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error in `books_get` {e}")


def authors_get(access_token, govdatahub="localhost:5000"):
    """
    GET /authors
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"http://{govdatahub}/authors"
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error in `authors_get` {e}")


def author_post(json_data, access_token, govdatahub="localhost:5000"):
    """
    POST /authors
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"http://{govdatahub}/authors"
    try:
        response = requests.post(url, json=json_data, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error in `author_post` {e}")


def author_get(author_id, access_token, govdatahub="localhost:5000"):
    """
    GET /authors
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"http://{govdatahub}/authors/{author_id}"
    try:
        response = requests.get(url, headers=headers)
        print(response)
        return response.json()
    except Exception as e:
        print(f"Error in `author_put` {e}")


def author_put(author_id, json_data, access_token, govdatahub="localhost:5000"):
    """
    PUT /authors
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"http://{govdatahub}/authors/{author_id}"
    try:
        response = requests.put(url, json=json_data, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error in `author_put` {e}")


def author_delete(author_id, access_token, govdatahub="localhost:5000"):
    """
    DELETE /authors/<id>
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"http://{govdatahub}/authors/{author_id}"
    try:
        response = requests.delete(url, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error in `authors_delete` {e}")


def categories_get(access_token, govdatahub="localhost:5000"):
    """
    GET /categories
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"http://{govdatahub}/categories"
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error in `categories_get`: {e}")


def category_get(category_id, access_token, govdatahub="localhost:5000"):
    """
    GET /categories/<id>
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"http://{govdatahub}/categories/{category_id}"
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error in `category_get`: {e}")


def category_post(json_data, access_token, govdatahub="localhost:5000"):
    """
    POST /categories
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"http://{govdatahub}/categories"
    try:
        response = requests.post(url, json=json_data, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error in `category_post`: {e}")


def category_put(category_id, json_data, access_token, govdatahub="localhost:5000"):
    """
    PUT /categories/<id>
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"http://{govdatahub}/categories/{category_id}"
    try:
        response = requests.put(url, json=json_data, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error in `category_put`: {e}")


def category_delete(category_id, access_token, govdatahub="localhost:5000"):
    """
    DELETE /categories/<id>
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"http://{govdatahub}/categories/{category_id}"
    try:
        response = requests.delete(url, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error in `category_delete`: {e}")


def download_file(filename, local_name, access_token, govdatahub="localhost:5000"):
    """GET /file/<id>"""
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"http://{govdatahub}/file/{filename}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        file_path = os.path.join("_download", local_name)
        with open(file_path, "wb") as f:
            f.write(response.content)
        return {"status": "success", "file_path": file_path}
    return {
        "status": "error",
        "message": f"Failed with status {response.status_code}",
    }


# Пример использования
if __name__ == "__main__":
    file_path = "fixtures/1.pdf"
    cover_path = "fixtures/1.png"
    ret = get_access_token("user1", "password1")
    access_token = ret.get("access_token")
    assert len(access_token) == 331, "Error in `get_access_token`"

    # Авторы
    for author in authors_get(access_token):
        ret = author_delete(author["id"], access_token)
    ret = authors_get(access_token)
    assert ret == [], "Error in `authors_get`"

    # Добавление автора
    json_data = {"name": "Ю.В. Китаев"}
    ret = author_post(json_data, access_token)
    author_id = ret.get("id")
    assert ret == {
        "id": 1,
        "name": "Ю.В. Китаев",
        "name_eng": None,
    }, "Error in `author_post`"
    assert author_id == 1, "Error in `author_post`"

    # Обновление автора
    json_data = {"name": "Ю.В. Китаев", "name_eng": "Kitayev Yu. V."}
    ret = author_put(author_id, json_data, access_token)
    assert ret == {
        "id": 1,
        "name": "Ю.В. Китаев",
        "name_eng": "Kitayev Yu. V.",
    }, "Error in `author_put`"

    # Книги
    for book in books_get(access_token):
        ret = book_delete(book["id"], access_token)
    ret = books_get(access_token)
    assert ret == [], "Error in `books_get`"

    # Загрузка файла
    book_dct = upload_file(file_path, access_token)
    book_id = book_dct.get("id")
    filename_orig = book_dct.get("filename_orig")
    assert book_dct == {
        "file_path": "uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf",
        "filename_orig": "1.pdf",
        "filename_uid": "3091401a1c74bfd441ace8d420f1e524.pdf",
        "id": "3091401a1c74bfd441ace8d420f1e524",
    }, "Error in `upload_file`"
    assert book_id == "3091401a1c74bfd441ace8d420f1e524", "Error in `upload_file`"
    assert filename_orig == "1.pdf", "Error in `upload_file`"

    # Обновление книги
    book_dct.update(
        {
            "title": "Перечень актуальных тематик диссертационных исследований в области наук об образовании",
            "isbn": "ISBN 987-6-5432-2345-6",
            "publication_date": "2023",
            "publisher": "РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ",
            "description": "Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова",
        }
    )
    ret = book_create(book_id, book_dct, access_token)
    assert ret == {
        "authors": [],
        "categories": [],
        "cover_image": None,
        "description": "Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова",
        "file_path": "uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf",
        "filename_orig": "1.pdf",
        "filename_uid": "3091401a1c74bfd441ace8d420f1e524.pdf",
        "id": "3091401a1c74bfd441ace8d420f1e524",
        "isbn": "ISBN 987-6-5432-2345-6",
        "publication_date": "2023",
        "publisher": "РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ",
        "telegram_file_id": None,
        "telegram_link": None,
        "title": "Перечень актуальных тематик диссертационных исследований в области наук об образовании",
    }, "Error in `book_create`"

    # Получение книги
    ret = book_get(book_id, access_token)
    assert ret == {
        "authors": [],
        "categories": [],
        "cover_image": None,
        "description": "Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова",
        "file_path": "uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf",
        "filename_orig": "1.pdf",
        "filename_uid": "3091401a1c74bfd441ace8d420f1e524.pdf",
        "id": "3091401a1c74bfd441ace8d420f1e524",
        "isbn": "ISBN 987-6-5432-2345-6",
        "publication_date": "2023",
        "publisher": "РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ",
        "telegram_file_id": None,
        "telegram_link": None,
        "title": "Перечень актуальных тематик диссертационных исследований в области наук об образовании",
    }, "Error in `book_get`"

    ret = books_get(access_token)
    assert ret == [
        {
            "authors": [],
            "categories": [],
            "cover_image": None,
            "description": "Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова",
            "file_path": "uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf",
            "filename_orig": "1.pdf",
            "filename_uid": "3091401a1c74bfd441ace8d420f1e524.pdf",
            "id": "3091401a1c74bfd441ace8d420f1e524",
            "isbn": "ISBN 987-6-5432-2345-6",
            "publication_date": "2023",
            "publisher": "РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ",
            "telegram_file_id": None,
            "telegram_link": None,
            "title": "Перечень актуальных тематик диссертационных исследований в области наук об образовании",
        }
    ], "Error in `books_get`"

    # Обновление книги
    json_data = {"title": "Список тем"}
    ret = book_update(book_id, json_data, access_token)
    assert ret == {
        "authors": [],
        "categories": [],
        "cover_image": None,
        "description": "Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова",
        "file_path": "uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf",
        "filename_orig": "1.pdf",
        "filename_uid": "3091401a1c74bfd441ace8d420f1e524.pdf",
        "id": "3091401a1c74bfd441ace8d420f1e524",
        "isbn": "ISBN 987-6-5432-2345-6",
        "publication_date": "2023",
        "publisher": "РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ",
        "telegram_file_id": None,
        "telegram_link": None,
        "title": "Список тем",
    }, "Error in `book_update`"

    # Обновление книги
    json_data = {"isbn": None}
    ret = book_update(book_id, json_data, access_token)
    assert ret == {
        "authors": [],
        "categories": [],
        "cover_image": None,
        "description": "Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова",
        "file_path": "uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf",
        "filename_orig": "1.pdf",
        "filename_uid": "3091401a1c74bfd441ace8d420f1e524.pdf",
        "id": "3091401a1c74bfd441ace8d420f1e524",
        "isbn": None,
        "publication_date": "2023",
        "publisher": "РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ",
        "telegram_file_id": None,
        "telegram_link": None,
        "title": "Список тем",
    }, "Error in `book_update`"

    # Обновление книги
    json_data = {"isbn": "ISBN 987-6-5432-2345-6"}
    ret = book_update(book_id, json_data, access_token)
    assert ret == {
        "authors": [],
        "categories": [],
        "cover_image": None,
        "description": "Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова",
        "file_path": "uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf",
        "filename_orig": "1.pdf",
        "filename_uid": "3091401a1c74bfd441ace8d420f1e524.pdf",
        "id": "3091401a1c74bfd441ace8d420f1e524",
        "isbn": "ISBN 987-6-5432-2345-6",
        "publication_date": "2023",
        "publisher": "РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ",
        "telegram_file_id": None,
        "telegram_link": None,
        "title": "Список тем",
    }, "Error in `book_update`"

    ret = book_get(book_id, access_token)
    assert ret == {
        "authors": [],
        "categories": [],
        "cover_image": None,
        "description": "Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова",
        "file_path": "uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf",
        "filename_orig": "1.pdf",
        "filename_uid": "3091401a1c74bfd441ace8d420f1e524.pdf",
        "id": "3091401a1c74bfd441ace8d420f1e524",
        "isbn": "ISBN 987-6-5432-2345-6",
        "publication_date": "2023",
        "publisher": "РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ",
        "telegram_file_id": None,
        "telegram_link": None,
        "title": "Список тем",
    }, "Error in `book_get`"

    ret = books_get(access_token)
    assert ret == [
        {
            "authors": [],
            "categories": [],
            "cover_image": None,
            "description": "Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова",
            "file_path": "uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf",
            "filename_orig": "1.pdf",
            "filename_uid": "3091401a1c74bfd441ace8d420f1e524.pdf",
            "id": "3091401a1c74bfd441ace8d420f1e524",
            "isbn": "ISBN 987-6-5432-2345-6",
            "publication_date": "2023",
            "publisher": "РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ",
            "telegram_file_id": None,
            "telegram_link": None,
            "title": "Список тем",
        }
    ], "Error in `books_get`"

    # Загрузка обложки
    ret = upload_file(cover_path, access_token)
    assert ret == {
        "file_path": "uploads/92/6d/926d51b67bd5143a49f70513bef45952.png",
        "filename_orig": "1.png",
        "filename_uid": "926d51b67bd5143a49f70513bef45952.png",
        "id": "926d51b67bd5143a49f70513bef45952",
    }, "Error in `file_upload`"

    # Обновление обложки книги
    json_data = {"cover_image": ret["file_path"]}
    ret = book_update(book_id, json_data, access_token)
    assert ret == {
        "authors": [],
        "categories": [],
        "cover_image": "uploads/92/6d/926d51b67bd5143a49f70513bef45952.png",
        "description": "Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова",
        "file_path": "uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf",
        "filename_orig": "1.pdf",
        "filename_uid": "3091401a1c74bfd441ace8d420f1e524.pdf",
        "id": "3091401a1c74bfd441ace8d420f1e524",
        "isbn": "ISBN 987-6-5432-2345-6",
        "publication_date": "2023",
        "publisher": "РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ",
        "telegram_file_id": None,
        "telegram_link": None,
        "title": "Список тем",
    }, "Error in `book_update`"

    # Обновление книги пустым словарем
    json_data = dict()
    ret = book_update(book_id, json_data, access_token)
    filename_uid = ret["filename_uid"]
    assert ret == {
        "authors": [],
        "categories": [],
        "cover_image": "uploads/92/6d/926d51b67bd5143a49f70513bef45952.png",
        "description": "Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова",
        "file_path": "uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf",
        "filename_orig": "1.pdf",
        "filename_uid": "3091401a1c74bfd441ace8d420f1e524.pdf",
        "id": "3091401a1c74bfd441ace8d420f1e524",
        "isbn": "ISBN 987-6-5432-2345-6",
        "publication_date": "2023",
        "publisher": "РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ",
        "telegram_file_id": None,
        "telegram_link": None,
        "title": "Список тем",
    }, "Error in `book_update`"

    # Загрузка списка книг
    ret = books_get(access_token)
    assert ret == [
        {
            "authors": [],
            "categories": [],
            "cover_image": "uploads/92/6d/926d51b67bd5143a49f70513bef45952.png",
            "description": "Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова",
            "file_path": "uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf",
            "filename_orig": "1.pdf",
            "filename_uid": "3091401a1c74bfd441ace8d420f1e524.pdf",
            "id": "3091401a1c74bfd441ace8d420f1e524",
            "isbn": "ISBN 987-6-5432-2345-6",
            "publication_date": "2023",
            "publisher": "РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ",
            "telegram_file_id": None,
            "telegram_link": None,
            "title": "Список тем",
        }
    ], "Error in `books_get`"

    # Скачивание книги
    ret = download_file(filename_uid, "1.pdf", access_token)
    assert ret == {'status': 'success', 'file_path': '_download/1.pdf'}, "Error in `download_file`"
    file_path = ret["file_path"]
    assert os.path.exists(file_path) is True, "Error in `f.write(ret.content)`"

    # Загрузка книги
    ret = book_get(book_id, access_token)
    book_id = ret.get("id")
    assert ret == {'authors': [], 'categories': [], 'cover_image': 'uploads/92/6d/926d51b67bd5143a49f70513bef45952.png', 'description': 'Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова', 'file_path': 'uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf', 'filename_orig': '1.pdf', 'filename_uid': '3091401a1c74bfd441ace8d420f1e524.pdf', 'id': '3091401a1c74bfd441ace8d420f1e524', 'isbn': 'ISBN 987-6-5432-2345-6', 'publication_date': '2023', 'publisher': 'РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ', 'telegram_file_id': None, 'telegram_link': None, 'title': 'Список тем'}, "Error in `book_get`"

    # Добавление автора в список авторов книги
    ret = add_author_to_book(book_id, author_id, access_token)
    assert ret == {'message': 'Author added to the book'}, "Error in `add_author_to_book`"

    # Загрузка книги
    ret = book_get(book_id, access_token)
    assert ret == {'authors': [{'id': 1, 'name': 'Ю.В. Китаев', 'name_eng': 'Kitayev Yu. V.'}], 'categories': [], 'cover_image': 'uploads/92/6d/926d51b67bd5143a49f70513bef45952.png', 'description': 'Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова', 'file_path': 'uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf', 'filename_orig': '1.pdf', 'filename_uid': '3091401a1c74bfd441ace8d420f1e524.pdf', 'id': '3091401a1c74bfd441ace8d420f1e524', 'isbn': 'ISBN 987-6-5432-2345-6', 'publication_date': '2023', 'publisher': 'РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ', 'telegram_file_id': None, 'telegram_link': None, 'title': 'Список тем'}, "Error in `book_get`"

    # Добавление автора в список авторов книги
    ret = add_author_to_book(book_id, author_id, access_token)
    assert ret == {'message': 'Author already added to the book'}, "Error in `add_author_to_book`"

    # Удаление автора из списка авторов книги
    ret = remove_author_from_book(book_id, author_id, access_token)
    assert ret == {'message': 'Author removed to the book'}, "Error in `remove_author_from_book`"

    # Загрузка книги
    ret = book_get(book_id, access_token)
    assert ret == {'authors': [], 'categories': [], 'cover_image': 'uploads/92/6d/926d51b67bd5143a49f70513bef45952.png', 'description': 'Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова', 'file_path': 'uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf', 'filename_orig': '1.pdf', 'filename_uid': '3091401a1c74bfd441ace8d420f1e524.pdf', 'id': '3091401a1c74bfd441ace8d420f1e524', 'isbn': 'ISBN 987-6-5432-2345-6', 'publication_date': '2023', 'publisher': 'РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ', 'telegram_file_id': None, 'telegram_link': None, 'title': 'Список тем'}, "Error in `book_get`"

    # Удаление автора из списка авторов книги
    ret = remove_author_from_book(book_id, author_id, access_token)
    assert ret == {'message': 'Author not found in the book'}, "Error in `remove_author_from_book`"

    # Удаление всех категорий
    ret = categories_get(access_token)
    for cat in ret:
        category_delete(cat["id"], access_token)

    ret = categories_get(access_token)
    assert ret == [], "Error in `categories_get`"

    ret = category_get(1, access_token)
    assert ret == {"message": "Category not found"}, "Error in `category_get`"

    ret = category_delete(1, access_token)
    assert ret == {"message": "Category not found"}, "Error in `category_delete`"

    # Создание новой категории
    json_data = {"name": "Классика"}
    ret = category_post(json_data, access_token)
    assert ret == {"id": 1, "name": "Классика"}, "Error in `category_post`"
    category_id = ret.get("id")

    # Переименование категории
    json_data = {"name": "Современная классика"}
    ret = category_put(category_id, json_data, access_token)
    assert ret == {"id": 1, "name": "Современная классика"}, "Error in `category_put`"

    # Добавление книги в категорию
    ret = add_category_to_book(book_id, category_id, access_token)
    assert ret == {
        "message": "Category added to the book"
    }, "Error in `add_category_to_book`"

    # Загрузка книги
    ret = book_get(book_id, access_token)
    assert ret == {'authors': [], 'categories': [{'id': 1, 'name': 'Современная классика'}], 'cover_image': 'uploads/92/6d/926d51b67bd5143a49f70513bef45952.png', 'description': 'Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова', 'file_path': 'uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf', 'filename_orig': '1.pdf', 'filename_uid': '3091401a1c74bfd441ace8d420f1e524.pdf', 'id': '3091401a1c74bfd441ace8d420f1e524', 'isbn': 'ISBN 987-6-5432-2345-6', 'publication_date': '2023', 'publisher': 'РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ', 'telegram_file_id': None, 'telegram_link': None, 'title': 'Список тем'}, "Error in `book_get`"

    ret = add_category_to_book(book_id, category_id, access_token)
    assert ret == {
        "message": "Category already added to the book"
    }, "Error in `add_category_to_book`"

    # Удаление книги из категории
    ret = remove_category_from_book(book_id, category_id, access_token)
    assert ret == {
        "message": "Category removed from the book"
    }, "Error in `remove_category_from_book`"

    ret = remove_category_from_book(book_id, category_id, access_token)
    assert ret == {
        "message": "Category not found in the book"
    }, "Error in `remove_category_from_book`"

    ret = category_delete(category_id, access_token)
    assert ret == {"message": "Category deleted"}, "Error in `category_delete`"

    ret = category_delete(category_id, access_token)
    assert ret == {"message": "Category not found"}, "Error in `category_delete`"

    # Удаление книги из категории
    ret = remove_category_from_book(book_id, category_id, access_token)
    assert ret == {
        "message": "Category not found"
    }, "Error in `remove_category_from_book`"

    # Удаление книги
    ret = book_delete(book_id, access_token)
    assert ret == {"message": "Book deleted"}, "Error in `book_delete`"

    # Удаление автора
    for author in authors_get(access_token):
        ret = author_delete(author["id"], access_token)
    ret = authors_get(access_token)
    assert ret == [], "Error in `authors_get`"
