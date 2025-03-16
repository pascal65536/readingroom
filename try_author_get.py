import requests
import json
import uuid

# GET /authors/<id> - получить информацию об авторе по ID.

author_id = "1"
url = f"http://localhost:5000/authors/{author_id}"
response = requests.get(url)

if response.status_code == 200:
    book = response.json()
    print("Информация об Авторе:", book)
else:
    print("Ошибка при получении информации об Авторе:", response.text)
