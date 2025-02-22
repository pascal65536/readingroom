import requests

# ID книги, которую вы хотите удалить
book_id = 'uuid_book_id'

# URL для удаления книги
url = f'http://localhost:5000/books/{book_id}'

# Отправка DELETE-запроса
response = requests.delete(url)

# Проверка ответа
if response.status_code == 200:
    print("Книга успешно удалена.")
else:
    print("Ошибка при удалении книги:", response.text)
