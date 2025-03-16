import requests

# GET /books - получить список всех книг.

# URL для получения списка книг
url = "http://localhost:5000/authors"

# Отправка GET-запроса
response = requests.get(url)

# Проверка ответа
if response.status_code != 200:
    print("Ошибка при получении списка авторов:", response.text)
    exit()

authors = response.json()
print("Список авторов:", authors)
