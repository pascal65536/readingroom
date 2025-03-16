import requests
import json
import os


def get_access_token(username, password):
    """
    POST /login
    """
    url = "http://localhost:5000/login"
    json_data = {"username": username, "password": password}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=json_data, headers=headers)
    try:
        response = requests.post(url, json=json_data, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error in `get_access_token` {e}")


def get_book_authors(book_id, access_token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    url = f"http://localhost:5000/books/{book_id}/authors"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        authors = response.json()
        print("Authors of the book:")
        for author in authors:
            print(f"- ID: {author['id']}, Name: {author['name']}")
    else:
        print("Error fetching authors:", response.text)


def add_author_to_book(book_id, author_id, access_token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    url = f"http://localhost:5000/books/{book_id}/authors"
    payload = {"author_id": author_id}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Author added to the book successfully.")
    else:
        print("Error adding author to the book:", response.text)


def remove_author_from_book(book_id, author_id, access_token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    url = f"http://localhost:5000/books/{book_id}/authors"
    payload = {"author_id": author_id}
    response = requests.delete(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Author removed from the book successfully.")
    else:
        print("Error removing author from the book:", response.text)



def book_get(book_id, access_token):
    """
    GET /books/<id>
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"http://localhost:5000/books/{book_id}"
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error in `book_get` {e}")


def book_update(book_id, json_data, access_token):
    """
    PUT /books/<id>
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"http://localhost:5000/books/{book_id}"
    try:
        response = requests.put(url, json=json_data, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error in `book_update` {e}")


def book_download(book_id, access_token):
    """
    GET /download/<id>
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"http://localhost:5000/download/{book_id}"
    try:
        response = requests.get(url, headers=headers)
        return response
    except Exception as e:
        print(f"Error in `book_download` {e}")


def book_delete(book_id, access_token):
    """
    DELETE /books/<id>
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"http://localhost:5000/books/{book_id}"
    try:
        response = requests.delete(url, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error in `book_delete` {e}")
            

def book_upload(file_path, access_token):
    """
    POST /upload
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = "http://localhost:5000/upload"
    json_data = {"title": file_path.split("/")[-1]}
    with open(file_path, "rb") as f:
        files = {"file": f}
        data = {"json_data": json.dumps(json_data)}
        try:
            response = requests.post(url, files=files, data=data, headers=headers)
            return response.json()
        except Exception as e:
            print(f"Error in `book_upload` {e}")


def books_get(access_token):
    """
    GET /books
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = "http://localhost:5000/books"
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error in `books_get` {e}")


def authors_get(access_token):
    """
    GET /authors
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = "http://localhost:5000/authors"
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error in `authors_get` {e}")


def author_post(json_data, access_token):
    """
    POST /authors
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = "http://localhost:5000/authors"
    try:
        response = requests.post(url, json=json_data, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error in `author_post` {e}")


def author_put(author_id, json_data, access_token):
    """
    PUT /authors
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"http://localhost:5000/authors/{author_id}"
    try:
        response = requests.put(url, json=json_data, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error in `author_put` {e}")


def authors_delete(author_id, access_token):
    """
    DELETE /authors/<id>
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"http://localhost:5000/authors/{author_id}"
    try:
        response = requests.delete(url, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error in `authors_delete` {e}")


# Пример использования
if __name__ == "__main__":
    file_path = "fixtures/Перечень актуальных тематик диссертационных исследований в области наук об образовании.pdf"
    ret = get_access_token("user1", "password1")
    access_token = ret.get("access_token")
    if not access_token:
        print(ret)
        exit()

    # Авторы
    for author in authors_get(access_token):
        ret = authors_delete(author['id'], access_token)
        print(ret)
    ret = authors_get(access_token)
    print("Authors of the base:", ret)

    json_data = {"name": "Ю.В. Китаев"}
    ret = author_post(json_data, access_token)
    author_id = ret.get("id")
    if not ret:
        print(ret)
        exit()
    print("Author of the book:", ret)

    json_data = {"name": "Ю.В. Китаев", "name_eng": "Kitayev Yu. V."}
    ret = author_put(author_id, json_data, access_token)
    if ret:
        print(ret)
        exit()
    print("Author of the book:", ret)
    exit()

    # Книги
    ret = books_get(access_token)
    if ret:
        print(ret)
        exit()

    ret = book_upload(file_path, access_token)
    book_id = ret.get("id")
    if book_id:
        ret = book_delete(book_id, access_token)
        print(ret)
    
    ret = book_upload(file_path, access_token)
    book_id = ret.get("id")
    filename_orig = ret.get("filename_orig")
    if not (book_id and  filename_orig):
        print(ret)
        exit()

    json_data = {
        "title": "Перечень актуальных тематик диссертационных исследований в области наук об образовании",
        "isbn": "ISBN 987-6-5432-2345-6",
        "publication_date": "2023",
        "publisher": "РОССИЙСКАЯ АКАДЕМИЯ ОБРАЗОВАНИЯ",
        "description": "Предисловие и. о. вице-президента РАО, Председателя ВАК при Минобрнауки России В. М. Филиппова",
    } 
    ret = book_update(book_id, json_data, access_token)
    book_id = ret.get("id")
    if not book_id:
        print(ret)
        exit()

    ret = books_get(access_token)
    if not ret:
        print(ret)
        exit()
    print(ret)

    ret = book_download(book_id, access_token)
    if ret.status_code != 200:
        print(ret)
        exit()

    # Сохранение файла на диск
    os.makedirs("_download", exist_ok=True)
    file_path = os.path.join("_download", filename_orig)
    with open(file_path, "wb") as f:
        f.write(ret.content)
    print("Файл успешно скачан.")

    ret = book_get(book_id, access_token)
    book_id = ret.get("id")
    if not book_id:
        print(ret)
        exit()

    ret = book_delete(book_id, access_token)
    book_id = ret.get("id")
    if not book_id:
        print(ret)
        exit()
    
    exit()

  

    

    book_id = "f6bc181c04dc44b906169ae87497435c"
    get_book_authors(book_id, access_token)

    # Добавление автора
    author_id_to_add = "author_id_here"
    add_author_to_book(book_id, author_id_to_add, access_token)

    # Удаление автора
    author_id_to_remove = "author_id_here"
    remove_author_from_book(book_id, author_id_to_remove, access_token)
