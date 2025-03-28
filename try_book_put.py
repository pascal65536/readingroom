import requests
import access


access_token = access.get_access_token("user1", "password1")
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}",
}

# PUT /books/<id> - обновить информацию о книге.
book_id = "05818e15ee46534594f36fdd3b1e1f7d"
url = f"http://localhost:5000/books/{book_id}"
json_data = {
    "title": "Базовые элементы цифровой техники: учебно-методическое пособие",
    "author_id": "Обновленный автор книги",
    "category_id": "Обновленная категория книги",
    "isbn": "ISBN 978-5-7996-2435-4",
    "publication_date": "11.09.2018",
    "publisher": "Екатеринбург. Издательство Уральского университета. 2018",
    "description": """В пособии последовательно изложены вопросы, относящиеся к элемент-
ной базе цифровой техники. Подробно рассматриваются основы схемотех-
ники различных базисных элементов и триггеров, анализируется работа
электронных схем. Особое внимание уделено методике создания логических
схем с помощью уравнений, связывающих входные и выходные состояния
элементов в различных импульсных устройствах.
Пособие предназначено для студентов университетов, не являющихся
профильными по специальностям, связанным с электротехникой и элек-
троникой. Оно также будет полезно достаточно широкому кругу читателей,
заинтересованных в получении знаний по электротехнике и основам ра-
диоэлектроники, а также в смежных с ними областях – цифровой технике
и робототехнике.""",
}
response = requests.put(url, json=json_data, headers=headers)
if response.status_code != 200:
    print("Ошибка при обновлении информации о книге:", response.text)
    exit()
updated_book = response.json()
print("Информация о книге обновлена:", updated_book)
