from models import Book
from extensions import db
from app import app

text = """
1. "1984" — Джордж Оруэлл
2. "Убить пересмешника" — Харпер Ли
3. "Мастер и Маргарита" — Михаил Булгаков
4. "Великий Гэтсби" — Фрэнсис Скотт Фицджеральд
5. "Преступление и наказание" — Федор Достоевский
6. "Гарри Поттер и философский камень" — Джоан Роулинг
7. "Сияние" — Стивен Кинг
8. "Анна Каренина" — Лев Толстой
9. "На западном фронте без перемен" — Эрих Мария Ремарк
10. "Маленький принц" — Антуан де Сент-Экзюпери
"""

book_lst = list()
for book_string in text.split("\n"):
    if not book_string:
        continue
    _, book_str = book_string.split(". ")
    title, author = book_str.split(" — ")
    title = title.strip('"')
    author = author.strip()
    print(title, author)
    book_lst.append(title)
print('-' * 50)

# """ Создать пустую БД в соответсвии с моделями """
# with app.app_context():
#     db.create_all()

# """ Создать несколько книг в БД """
# with app.app_context():
#     for title in book_lst:
#         book_obj = Book(title=title)
#         db.session.add(book_obj)
#         db.session.commit()

# """ Получить все книги из БД """
# with app.app_context():
#     book_qs = Book.query.all()
#     print(book_qs)

# """ Получить книги по названиям """
# with app.app_context():
#     title_lst = ['Мастер и Маргарита', 'Преступление и наказание', 'Гарри Поттер и философский камень']
#     book_qs = Book.query.filter(Book.title.in_(title_lst)).all()
#     print(book_qs)

# """ Получить книгу по названию """
# with app.app_context():
#     title = 'Мастер и Маргарита'
#     book_qs = Book.query.filter(Book.title.like(title)).all()
#     print(book_qs)

# """ Получить книгу по части названия """
# with app.app_context():
#     title_part = '%пере%'
#     book_qs = Book.query.filter(Book.title.like(title_part)).all()
#     print(book_qs)

# """ И """
# with app.app_context():
#     book_qs = Book.query.filter(Book.title.like('%ф%'), Book.title.like('%й%')).all()
#     print(book_qs)    

# """ ИЛИ """
# with app.app_context():
#     book_qs = Book.query.filter(Book.title.like('%ф%') | Book.title.like('%й%')).all()
#     print(book_qs)

# """ GTE """
# with app.app_context():
#     book_qs = Book.query.filter(Book.id >= 5).all()
#     print(book_qs)    

# """ LT """
# with app.app_context():
#     book_qs = Book.query.filter(Book.id < 5).all()
#     print(book_qs)        