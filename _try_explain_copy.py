from utils import get_access_token, books_get, book_delete,book_upload, authors_get, author_post, author_get, author_put, authors_delete, categories_get, category_get, category_post, category_put, category_delete, get_book_categories, add_category_to_book, remove_category_from_book


ret = get_access_token("user1", "password1")
access_token = ret.get("access_token")

ret = categories_get(access_token)
for cat in ret:
    category_delete(cat['id'], access_token)

ret = categories_get(access_token)
assert ret == [], "Error in `categories_get`"

ret = category_get(1, access_token)
assert ret == {'message': 'Category not found'}, "Error in `category_get`"

ret = category_delete(1, access_token)
assert ret == {'message': 'Category not found'}, "Error in `category_delete`"

# Создание новой категории
json_data = {"name": "Классика"}
ret = category_post(json_data, access_token)
assert ret == {'id': 1, 'name': 'Классика'}, "Error in `category_post`"
category_id = ret.get("id")

# Переименование категории
json_data = {"name": "Современная классика"}
ret = category_put(category_id, json_data, access_token)
assert ret == {'id': 1, 'name': 'Современная классика'}, "Error in `category_put`"

# Книги
for book in books_get(access_token):
    ret = book_delete(book['id'], access_token)
ret = books_get(access_token)
assert ret==[], "Error in `books_get`"

# Загрузка книги
file_path = "fixtures/Перечень актуальных тематик диссертационных исследований в области наук об образовании.pdf"
ret = book_upload(file_path, access_token)
book_id = ret.get("id")
filename_orig = ret.get("filename_orig")
assert ret == {'file_path': 'uploads/30/91/3091401a1c74bfd441ace8d420f1e524.pdf', 'filename_orig': 'Перечень актуальных тематик диссертационных исследований в области наук об образовании.pdf', 'filename_uid': '3091401a1c74bfd441ace8d420f1e524.pdf', 'id': '3091401a1c74bfd441ace8d420f1e524', 'title': 'Перечень актуальных тематик диссертационных исследований в области наук об образовании.pdf'}, "Error in `book_upload`"
assert book_id == '3091401a1c74bfd441ace8d420f1e524', "Error in `book_upload`"
assert filename_orig == 'Перечень актуальных тематик диссертационных исследований в области наук об образовании.pdf', "Error in `book_upload`"
    


# Добавление книги в категорию
ret = add_category_to_book(book_id, category_id, access_token)
assert ret == {'message': 'Category added to the book'}, "Error in `add_category_to_book`"

ret = add_category_to_book(book_id, category_id, access_token)
assert ret == {'message': 'Category already added to the book'}, "Error in `add_category_to_book`"

# Удаление книги из категории
ret = remove_category_from_book(book_id, category_id, access_token)
assert ret == {'message': 'Category removed from the book'}, "Error in `remove_category_from_book`"

ret = remove_category_from_book(book_id, category_id, access_token)
assert ret == {'message': 'Category not found in the book'}, "Error in `remove_category_from_book`"

ret = category_delete(category_id, access_token)
assert ret == {'message': 'Category deleted'}, "Error in `category_delete`"


ret = category_delete(category_id, access_token)
assert ret == {'message': 'Category not found'}, "Error in `category_delete`"

# Удаление книги из категории
ret = remove_category_from_book(book_id, category_id, access_token)
assert ret == {'message': 'Category not found'}, "Error in `remove_category_from_book`"
