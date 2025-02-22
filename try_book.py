import requests

# GET /books - получить список всех книг.

# URL для получения списка книг
url = "http://localhost:5000/books"

# Отправка GET-запроса
response = requests.get(url)

# Проверка ответа
if response.status_code != 200:
    print("Ошибка при получении списка книг:", response.text)
    exit()

books = response.json()
print("Список книг:", books)
