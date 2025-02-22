import requests

# URL для получения списка книг
url = 'http://localhost:5000/books'

# Отправка GET-запроса
response = requests.get(url)

# Проверка ответа
if response.status_code == 200:
    books = response.json()
    print("Список книг:", books)
else:
    print("Ошибка при получении списка книг:", response.text)
