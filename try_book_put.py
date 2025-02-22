import requests

# PUT /books/<id> - обновить информацию о книге.

# ID книги, информацию о которой вы хотите обновить
book_id = '524fc290636f207b73b0da18632dc909'

# URL для обновления информации о книге
url = f'http://localhost:5000/books/{book_id}'

# Обновленные данные книги в формате JSON
json_data = {
    "title": "Обновленное название книги",
    "author_id": "Обновленное автор книги",
    "category_id": "Обновленная категория книги"
}

# Отправка PUT-запроса с данными
response = requests.put(url, json=json_data)

# Проверка ответа
if response.status_code != 200:
    print("Ошибка при обновлении информации о книге:", response.text)
    exit()
    
updated_book = response.json()
print("Информация о книге обновлена:", updated_book)
