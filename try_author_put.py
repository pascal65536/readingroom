import requests
import json
import uuid

# PUT /authors/<id> - обновить информацию об авторе.

author_id = "4"
url = f"http://localhost:5000/authors/{author_id}"
headers = {"Content-Type": "application/json"}
json_data = {"name": "Китаев Ю.В.", "name_eng": "Kitayev Yu. V."}
response = requests.put(url, json=json_data, headers=headers)

if response.status_code == 200:
    book = response.json()
    print("Информация об Авторе:", book)
else:
    print("Ошибка при получении информации об Авторе:", response.text)
