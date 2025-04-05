import os
import requests
import hashlib

q = "Большая книга проектов Python"
url = f"https://www.googleapis.com/books/v1/volumes?q={q}"
print(url)

ret = requests.get(url)
if ret.status_code == 200:
    book_dct = ret.json()
    for book in book_dct["items"]:
        print(book["volumeInfo"]["title"])
        if q == book["volumeInfo"]["title"]:
            print(book)

