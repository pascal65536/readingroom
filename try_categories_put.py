import requests
import json
import uuid

# PUT /categories/<id> - обновить информацию о категории.

category_id = "58f2b7d4-72ca-4ea1-a3b9-71c5066795f5" #так как это вроде пример я не меняла
url = f"http://localhost:5000/categories/{category_id}"
headers = {"Content-Type": "application/json"}
json_data2 = {"category": "экшн", "name_eng": "action"}
response = requests.put(url, json=json_data2, headers=headers)

if response.status_code == 200:
    book = response.json()
    print("Информация о категории:", book)
else:
    print("Ошибка при получении информации о категории:", response.text)
