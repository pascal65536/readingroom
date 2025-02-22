import requests

# URL для создания новой книги
url = 'http://localhost:5000/books'

# Данные новой книги в формате JSON
json_data = {
    "title": "Новая книга",
    "author_id": "uuid_author_id",
    "category_id": "uuid_category_id"
}

# Отправка POST-запроса с данными
response = requests.post(url, json=json_data)

# Проверка ответа
if response.status_code == 201:
    new_book = response.json()
    print("Новая книга создана:", new_book)
else:
    print("Ошибка при создании книги:", response.text)
