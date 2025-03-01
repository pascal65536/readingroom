import requests
import os

# GET /books/<id> - получить информацию о книге по ID.

# ID книги, информацию о которой вы хотите получить
book_id = "475857144ab65f9c8a2857d06452f167"

# URL для получения информации о книге
url = f"http://localhost:5000/books/{book_id}"

# Отправка GET-запроса
response = requests.get(url)

# Проверка ответа
if response.status_code != 200:
    print("Ошибка при получении информации о книге:", response.text)
    exit()

book = response.json()
filename_orig = book["filename_orig"]


# GET /download/<id> - скачать PDF-файл книги.

# URL для скачивания файла
url = f"http://localhost:5000/download/{book_id}"

# Отправка GET-запроса для скачивания файла
response = requests.get(url)

# Проверка ответа
if response.status_code != 200:
    print("Ошибка при скачивании файла:", response.text)
    exit()

# Сохранение файла на диск
os.makedirs("_download", exist_ok=True)
file_path = os.path.join("_download", filename_orig)
with open(file_path, "wb") as f:
    f.write(response.content)
print("Файл успешно скачан.")
