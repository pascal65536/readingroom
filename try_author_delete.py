import requests
import json
import uuid

# DELETE /authors/<id> - удалить автора.

author_id = "2"
url = f"http://localhost:5000/authors/{author_id}"
response = requests.delete(url)

if response.status_code == 200:
    book = response.json()
    print("Информация об Авторе:", book)
else:
    print("Ошибка при получении информации об Авторе:", response.text)
