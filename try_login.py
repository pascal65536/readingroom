import requests

# URL для получения
url = "http://govdatahub.ru/login"
# Отправка POST-запроса
json_data = {"username": "user1", "password": "password1"}
headers = {"Content-Type": "application/json"}
response = requests.post(url, json=json_data, headers=headers)
# Проверка ответа
if response.status_code != 200:
    print("Ошибка при получении списка книг:", response.text)
    exit()

access_token_json = response.json()
access_token = access_token_json["access_token"]

# GET /protected - получить
url = "http://govdatahub.ru/protected"
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
response = requests.get(url, headers=headers)

# Проверка ответа
if response.status_code != 200:
    print("Ошибка при доступе к скрытой части сайта:", response.text)
    exit()

# URL для получения списка книг
url = "http://govdatahub.ru/authors"
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
# Отправка GET-запроса
response = requests.get(url, headers=headers)

# Проверка ответа
if response.status_code != 200:
    print("Ошибка при получении списка авторов:", response.text)
    exit()

authors = response.json()
print("Список авторов:", authors)
