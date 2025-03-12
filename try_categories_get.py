import requests
import json
import uuid

# GET /categories/<id> - получить информацию о категории по ID.

category_id = "49da3554-608c-4f12-aa2f-81bc39b20c81" #так как это вроде пример я не меняла
url = f"http://localhost:5000/categories/{category_id}"
response = requests.get(url)

if response.status_code == 200:
    book = response.json()
    print("Информация о категории:", book)
else:
    print("Ошибка при получении информации о категории:", response.text)
