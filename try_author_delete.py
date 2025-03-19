import requests
import json
import uuid
import access


access_token = access.get_access_token("user1", "password1")
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}",
}


# DELETE /authors/<id> - удалить автора.
author_id = "4"
url = f"http://localhost:5000/authors/{author_id}"
response = requests.delete(url, headers=headers)

if response.status_code == 200:
    book = response.json()
    print("Информация об Авторе:", book)
else:
    print("Ошибка при получении информации об Авторе:", response.text)
