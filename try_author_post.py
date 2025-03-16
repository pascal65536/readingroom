import requests
import json
import uuid

# POST /authors - добавить нового автора.

url = "http://localhost:5000/authors"
json_data = {"name": "Ю.В. Китаев"}
headers = {"Content-Type": "application/json"}
response = requests.post(url, json=json_data, headers=headers)

if response.status_code == 200:
    book = response.json()
    print("Информация об Авторе:", book)
else:
    print("Ошибка при получении информации об Авторе:", response.text)
