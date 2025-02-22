import requests

# ID книги, файл которой вы хотите скачать
book_id = '29eef3cd-229f-4356-a316-bca70d59c141'

# URL для скачивания файла
url = f'http://localhost:5000/download/{book_id}'

# Отправка GET-запроса для скачивания файла
response = requests.get(url)

# Проверка ответа
if response.status_code == 200:
    # Сохранение файла на диск
    with open('downloaded_book.pdf', 'wb') as f:
        f.write(response.content)
    print("Файл успешно скачан.")
else:
    print("Ошибка при скачивании файла:", response.text)
