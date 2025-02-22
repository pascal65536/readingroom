import requests

# ID книги, информацию о которой вы хотите обновить
book_id = '29eef3cd-229f-4356-a316-bca70d59c141'

# URL для обновления информации о книге
url = f'http://localhost:5000/books/{book_id}'

# Обновленные данные книги в формате JSON
json_data = {
    "title": "Обновленное название книги",
    "author_id": "new_uuid_author_id"
}

# Отправка PUT-запроса с данными
response = requests.put(url, json=json_data)

# Проверка ответа
if response.status_code == 200:
    updated_book = response.json()
    print("Информация о книге обновлена:", updated_book)
else:
    print("Ошибка при обновлении информации о книге:", response.text)
