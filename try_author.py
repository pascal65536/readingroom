import requests

# GET /books - получить список всех книг.
url = "http://localhost:5000/authors"
response = requests.get(url)
if response.status_code != 200:
    print("Ошибка при получении списка авторов:", response.text)
    exit()
authors = response.json()
print("Список авторов:", authors)
