import requests

# DELETE /books/<id> - удалить книгу.

# ID книги, информацию о которой вы хотите обновить
book_id = '524fc290636f207b73b0da18632dc909'

# URL для удаления книги
url = f'http://localhost:5000/books/{book_id}'

# Отправка DELETE-запроса
response = requests.delete(url)

# Проверка ответа
if response.status_code == 200:
    print("Книга успешно удалена.")
else:
    print("Ошибка при удалении книги:", response.text)
