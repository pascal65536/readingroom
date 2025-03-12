import requests
import json
import uuid

# POST /categories - добавить новую категорию.

url = "http://127.0.0.1:5000/categories"
json_data2 = {"category": "python"}
headers = {"Content-Type": "application/json"}
response = requests.post(url, json=json_data2, headers=headers)

if response.status_code == 200:
    book = response.json()
    print("Информация о категории:", book)
else:
    print("Ошибка при получении информации о категории:", response.text)
