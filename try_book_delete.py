import requests
import access


access_token = access.get_access_token("user1", "password1")
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}",
}


# DELETE /books/<id> - удалить книгу.
book_id = "f6bc181c04dc44b906169ae87497435c"
url = f"http://localhost:5000/books/{book_id}"
response = requests.delete(url, headers=headers)
if response.status_code == 200:
    print("Книга успешно удалена.")
else:
    print("Ошибка при удалении книги:", response.text)
