import requests
import json
import uuid

# PUT /authors/<id> - обновить информацию об авторе.

author_id = "c727b585-b684-4d2f-a8ca-4e4dab2d1c55"
url = f"http://localhost:5000/authors/{author_id}"
headers = {"Content-Type": "application/json"}
json_data = {"name": "Марк Твен", "name_eng": "Mark Twain"}
response = requests.put(url, json=json_data, headers=headers)

if response.status_code == 200:
    book = response.json()
    print("Информация об Авторе:", book)
else:
    print("Ошибка при получении информации об Авторе:", response.text)
