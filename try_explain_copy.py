from utils import get_access_token, authors_get, author_post, author_get, author_put, authors_delete, categories_get, category_get, category_post, category_put, category_delete, get_book_categories, add_category_to_book, remove_category_from_book


ret = get_access_token("user1", "password1")
access_token = ret.get("access_token")
print(access_token)

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

# Удаление категории
ret = category_delete(category_id, access_token)
assert ret == {'message': 'Category deleted'}, "Error in `category_delete`"

# Добавление книги в категорию
book_id = 1  # Пример ID книги
ret = add_category_to_book(book_id, category_id, access_token)
print("Книга добавлена в категорию:", ret)

# Удаление книги из категории
ret = remove_category_from_book(book_id, category_id, access_token)
print("Книга удалена из категории:", ret)