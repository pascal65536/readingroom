import requests

# ID книги, информацию о которой вы хотите получить
book_id = '29eef3cd-229f-4356-a316-bca70d59c141'

# URL для получения информации о книге
url = f'http://localhost:5000/books/{book_id}'

# Отправка GET-запроса
response = requests.get(url)

# Проверка ответа
if response.status_code == 200:
    book = response.json()
    print("Информация о книге:", book)
else:
    print("Ошибка при получении информации о книге:", response.text)
