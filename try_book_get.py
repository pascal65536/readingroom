import requests


# GET /books/<id> - получить информацию о книге по ID.
book_id = "05818e15ee46534594f36fdd3b1e1f7d"
url = f"http://localhost:5000/books/{book_id}"
response = requests.get(url)
if response.status_code != 200:
    print("Ошибка при получении информации о книге:", response.text)
    exit()
book = response.json()
print("Информация о книге:", book)
