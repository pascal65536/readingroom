import requests

# ID книги, информацию о которой вы хотите получить
book_id = "524fc290636f207b73b0da18632dc909"

# URL для получения информации о книге
url = f"http://localhost:5000/books/{book_id}"

# Отправка GET-запроса
response = requests.get(url)

# Проверка ответа
if response.status_code != 200:
    print("Ошибка при получении информации о книге:", response.text)
    exit()

book = response.json()
print("Информация о книге:", book)
