import requests
import json
import uuid
import access


access_token = access.get_access_token("user1", "password1")
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}",
}


# POST /authors - добавить нового автора.
url = "http://localhost:5000/authors"
json_data = {"name": "Ю.В. Китаев"}
response = requests.post(url, json=json_data, headers=headers)
if response.status_code == 200:
    book = response.json()
    print("Информация об Авторе:", book)
else:
    print("Ошибка при получении информации об Авторе:", response.text)
