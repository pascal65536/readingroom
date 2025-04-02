from utils import get_access_token, authors_get, author_post, author_get, author_put, authors_delete, categories_get, category_get, category_post, category_put, category_delete, get_book_categories, add_category_to_book, remove_category_from_book


ret = get_access_token("user1", "password1")
access_token = ret.get("access_token")
print(access_token)

ret = authors_get(access_token)
print(ret)

json_data = {"name": "А.С. Пушкин"}
ret = author_post(json_data, access_token)
print(ret)


ret = author_get('1', access_token)
print(ret)
ret = author_get('2', access_token)
print(ret)


json_data = {"name": "А.С. Пушкин", "name_eng": "Alexander Pushkin"}
ret = author_put('2', json_data, access_token)
print(ret)

ret = author_get('2', access_token)
print(ret)


ret = authors_delete('2', access_token)
print(ret)

ret = author_get('2', access_token)
print(ret)

# Запрос всех категорий
ret = categories_get(access_token)
print("Все категории:", ret)

# Удаление всех категорий, если они есть
for category in ret:
    category_id = category.get("id")
    if category_id:
        del_ret = category_delete(category_id, access_token)
        print(f"Удалена категория {category_id}:", del_ret)

# Создание новой категории
json_data = {"name": "Классика"}
ret = category_post(json_data, access_token)
print("Создана категория:", ret)
category_id = ret.get("id")

# Переименование категории
json_data = {"name": "Современная классика"}
ret = category_put(category_id, json_data, access_token)
print("Категория переименована:", ret)

# Удаление категории
ret = category_delete(category_id, access_token)
print("Категория удалена:", ret)

# Добавление книги в категорию
book_id = 1  # Пример ID книги
ret = add_category_to_book(book_id, category_id, access_token)
print("Книга добавлена в категорию:", ret)

# Удаление книги из категории
ret = remove_category_from_book(book_id, category_id, access_token)
print("Книга удалена из категории:", ret)