import requests

# GET /books - получить список всех книг.
url = "http://localhost:5000/books"
response = requests.get(url)
if response.status_code != 200:
    print("Ошибка при получении списка книг:", response.text)
    exit()
books = response.json()
print("Список книг:", books)
