import os
import requests
import hashlib

q = "Дэвид Сэломон. Сжатие данных, изображений и звука"
url = f"https://www.googleapis.com/books/v1/volumes?q={q}"

ret = requests.get(url)
if ret.status_code == 200:
    book_dct = ret.json()
    for book in book_dct["items"]:
        print(book["volumeInfo"]["title"])
        if q == book["volumeInfo"]["title"]:
            print(book)

