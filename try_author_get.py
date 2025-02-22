import requests
import json
import uuid

# GET /authors/<id> - получить информацию об авторе по ID.

author_id = "c727b585-b684-4d2f-a8ca-4e4dab2d1c55"
url = f"http://localhost:5000/authors/{author_id}"
response = requests.get(url)

if response.status_code == 200:
    book = response.json()
    print("Информация об Авторе:", book)
else:
    print("Ошибка при получении информации об Авторе:", response.text)
