import requests
import json
import uuid

# DELETE /categories/<id> - удалить категорию.

category_id = "58f2b7d4-72ca-4ea1-a3b9-71c5066795f5" #так как это вроде пример я не меняла
url = f"http://localhost:5000/categories/{category_id}"
response = requests.delete(url)

if response.status_code == 200:
    book = response.json()
    print("Информация о категории:", book)
else:
    print("Ошибка при получении информации о категории:", response.text)