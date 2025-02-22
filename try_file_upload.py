import requests
import json
import os

url = 'http://localhost:5000/upload'

file_path = '/home/pascal65536/Загрузки/1.pdf'

json_data = {
    "title": "Моя книга",
    "author_id": "uuid_author_id",
    "category_id": "uuid_category_id"
}

with open(file_path, 'rb') as f:
    # files = {'file': (os.path.basename(file_path), f)}
    files = {'file': f}
    data = {'json_data': json.dumps(json_data)}
    response = requests.post(url, files=files, data=data)

print(response.status_code)


# Проверка ответа
# if response.status_code == 200 or response.status_code == 201:
#     print("Файл успешно загружен:", response.json())
# else:
#     print("Ошибка при загрузке файла:", response.text)
