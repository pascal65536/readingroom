import requests
import json
import uuid

# GET /authors/<id> - получить информацию об авторе по ID.

author_id = "49da3554-608c-4f12-aa2f-81bc39b20c81"
url = f"http://localhost:5000/authors/{author_id}"
response = requests.get(url)

if response.status_code == 200:
    book = response.json()
    print("Информация об Авторе:", book)
else:
    print("Ошибка при получении информации об Авторе:", response.text)
