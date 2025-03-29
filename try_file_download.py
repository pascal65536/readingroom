import requests
import os
import access


access_token = access.get_access_token("user1", "password1")
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}",
}

# GET /books/<id> - получить информацию о книге по ID.

# ID книги, информацию о которой вы хотите получить
book_id = "524fc290636f207b73b0da18632dc909"

# URL для получения информации о книге
url = f"http://localhost:5000/books/{book_id}"
response = requests.get(url, headers=headers)
if response.status_code != 200:
    print("Ошибка при получении информации о книге:", response.text)
    exit()

book = response.json()
filename_orig = book["filename_orig"]

# GET /download/<id> - скачать PDF-файл книги.
url = f"http://localhost:5000/download/{book_id}"
response = requests.get(url, headers=headers)
if response.status_code != 200:
    print("Ошибка при скачивании файла:", response.text)
    exit()
# Сохранение файла на диск
os.makedirs("_download", exist_ok=True)
file_path = os.path.join("_download", filename_orig)
with open(file_path, "wb") as f:
    f.write(response.content)
print("Файл успешно скачан.")
