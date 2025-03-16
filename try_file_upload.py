import requests
import json
import os
import access


access_token = access.get_access_token("user1", "password1")
headers = {
    "Authorization": f"Bearer {access_token}",
}


# POST /upload - загрузить PDF-файл книги.
url = "http://localhost:5000/upload"
file_path = (
    "/home/pacal65536/Yandex.Disk/Books/Леонтьев Юрий - Word_2003.pdf"
)
json_data = {"title": file_path.split("/")[-1], "author_id": None, "category_id": None}
with open(file_path, "rb") as f:
    files = {"file": f}
    data = {"json_data": json.dumps(json_data)}
    response = requests.post(url, files=files, data=data, headers=headers)
# Проверка ответа
if response.status_code not in [200, 201]:
    print("Ошибка при загрузке файла:", response.text)
    exit()
print("Файл успешно загружен:", response.json())
