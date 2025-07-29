from extensions import db
from app import app
from model import (
    File, FileHead, FileData,
    GeoAddress,
    Author, OriginalBook, AuthorBook,
    Publisher, Book,
    User, UserAuthor, Grade,
    CustomBook, UserCustomBook,
    Group, UserGroup,
    Message, BookDistribution, Order,
)

# text = """
# Лев Толстой | 1828-09-09 | 1910-11-20 | Россия, Тульская обл., Ясная Поляна, ул. Усадьба Толстого, 1, - | 54.075383, 37.524900 | 301214
# Фёдор Достоевский | 1821-11-11 | 1881-02-09 | Россия, Москва, ул. Достоевского, 2, 10 | 55.781758, 37.614015 | 105005
# Антон Чехов | 1860-01-29 | 1904-07-15 | Россия, Ростовская обл., Таганрог, ул. Чехова, 69, - | 47.209418, 38.937481 | 347900
# Александр Пушкин | 1799-06-06 | 1837-02-10 | Россия, Москва, ул. Пречистенка, 12/2, - | 55.740833, 37.595278 | 119034
# Михаил Лермонтов | 1814-10-15 | 1841-07-27 | Россия, Пензенская обл., с. Тарханы, Музей-заповедник, 1, - | 53.213056, 45.269444 | 442280
# Николай Гоголь | 1809-04-01 | 1852-03-04 | Украина, Полтавская обл., с. Великие Сорочинцы, ул. Гоголя, 1, - | 50.023056, 33.915556 | 38000
# Иван Тургенев | 1818-11-09 | 1883-09-03 | Россия, Орловская обл., Орёл, ул. Тургенева, 11, - | 52.965278, 36.064444 | 302028
# Александр Солженицын | 1918-12-11 | 2008-08-03 | Россия, Ставропольский край, Кисловодск, ул. Солженицына, 12, 5 | 43.905556, 42.715000 | 357700
# Борис Пастернак | 1890-02-10 | 1960-05-30 | Россия, Московская обл., пос. Переделкино, ул. Пастернака, 3, - | 55.651389, 37.338056 | 142784
# Анна Ахматова | 1889-06-23 | 1966-03-05 | Россия, Санкт-Петербург, наб. реки Фонтанки, 34, 3 | 59.934167, 30.342500 | 191014
# """

# text = [[i.strip() for i in line.split('|')] for line in text.split("\n") if line]
# geo_address = [
#     (*line[3].split(', '), *map(float, line[4].split(', ')), int(line[5]))
#     for line in text
# ]
# author = [(line[0], line[1], line[2]) for line in text]
# print(*author, sep='\n')


""" Создать пустую БД в соответсвии с моделями """
with app.app_context():
    db.create_all()

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