from extensions import db
# db: (
#     Model, Column, ForeignKey,
#     Boolean, db.Integer, Numeric,
#     String, Text,
#     Date, DateTime
# )


# class File(db.Model): ...
# class FileHead(db.Model): ...
# class FileData(db.Model): ...

# class GeoAddress(db.Model): ...

# class Author(db.Model): ...
# class AuthorBook(db.Model): ...
# class OriginalBook(db.Model): ...

# class Publisher(db.Model): ...
# class Book(db.Model): ...

# class User(db.Model): ...
# class UserAuthor(db.Model): ...
# class Grade(db.Model): ...

# class CustomBook(db.Model): ...
# class UserCustomBook(db.Model): ...

# class Group(db.Model): ...
# class UserGroup(db.Model): ...
# class Message(db.Model): ...

# class BookDistribution(db.Model): ...
# class Order(db.Model): ...



class File(db.Model):
    __tablename__ = "file"
  
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    head_id = db.Column(db.Integer, db.ForeignKey("file_head"), nullable=False, index=True)
    data_id = db.Column(db.Integer, db.ForeignKey("file_data"), nullable=False, index=True)


class FileHead(db.Model):
    """
    Заголовок файла - данные (обычно визуальные), которуе может исменить пользователь
    (это позволяет разным пользователям иметь один файл с разным иминем)
    """
    __tablename__ = "file_head"
  
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    name = db.Column(db.String(255))
    ...


class FileData(db.Model):
    """
    Данные неизменяемые пользователем
    """
    __tablename__ = "file_data"
  
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    path = db.Column(db.String(255), unique=True, nullable=False)
    # count = db.Column(db.Integer, nullable=False)  # Подсчёт ссылок в случае, если мы будем автоматически удалять неиспользуемый файл



class GeoAddress(db.Model):
    __tablename__ = "geo_address"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    country = db.Column(db.String(63))
    region = db.Column(db.String(63))
    city = db.Column(db.String(63))
    street = db.Column(db.String(127))
    building = db.Column(db.String(20))
    apartment = db.Column(db.String(20))
    # Координаты (для карт)
    latitude = db.Column(db.Numeric(9, 6))  # Широта: 90.000000
    longitude = db.Column(db.Numeric(9, 6)) # Долгота: 180.000000
    # Почтовый индекс
    postal_code = db.Column(db.String(16))



class Author(db.Model):
    __tablename__ = "author"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    name = db.Column(db.String(31), nullable=False)
    date_birth = db.Column(db.Date, index=True)
    date_death = db.Column(db.Date, index=True)
    address_id = db.Column(db.Integer, db.ForeignKey("geo_address"), index=True)



class OriginalBook(db.Model):
    __tablename__ = "оriginal_book"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    name = db.Column(db.String(255))
    writing_date = db.Column(db.Date, index=True)
    # Если понадобится оригинальный текст
    # text = db.Column(db.Integer, db.ForeignKey("file"), unique=True) | db.Column(db.Integer, db.Text, unique=True, nullable=False)


class AuthorBook(db.Model):
    """
    Таблица для связи автора и первоисточника
    У книги можт быть несколько авторов
    """
    __tablename__ = "author_book"
    
    author_id = db.Column(db.Integer, db.ForeignKey("author"), primary_key=True, nullable=False, index=True)
    оriginal_book_id = db.Column(db.Integer, db.ForeignKey("оriginal_book"), primary_key=True, nullable=False, index=True)



class Publisher(db.Model):
    __tablename__ = "publisher"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    name = db.Column(db.String(31), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey("geo_address"), index=True)


class Book(db.Model):
    __tablename__ = "book"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    isbn = db.Column(db.String(13), unique=True)
    title = db.Column(db.Text())
    original_id = db.Column(db.Integer, db.ForeignKey("оriginal_book"), nullable=False, index=True)
    cover_id = db.Column(db.Integer, db.ForeignKey("file"), index=True)
    text_id = db.Column(db.Integer, db.ForeignKey("file"), nullable=False, index=True)
    publisher_id = db.Column(db.Integer, db.ForeignKey("publisher"), index=True)
    publication_date = db.Column(db.Date, nullable=False, index=True)
    count_copy = db.Column(db.Integer, nullable=False) # количество ссылок, может быть полезно для статистики



class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    name = db.Column(db.String(63))
    login = db.Column(db.String(63), nullable=False, unique=True)
    password = db.Column(db.String(63), nullable=False)
    avatar = db.Column(db.Integer, db.ForeignKey("file"), index=True)
    title = db.Column(db.Text())
    email = db.Column(db.String(320))
    ...


class UserAuthor(db.Model):
    """
    Пользователь может быть несколькими авторами (псевдонимы)
    Также, в редких случаях, и несколько пользователей могут быть одним автором
    """
    __tablename__ = "user_author"

    user_id = db.Column(db.Integer, db.ForeignKey("User"), primary_key=True, nullable=False, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey("Author"), primary_key=True, nullable=False, index=True)


class Grade(db.Model):
    """
    Оценка книг пользователями, вычисляется как среднее числительное
    Возможно будет долго вычислятся
    """
    __tablename__ = "grade"

    user_id = db.Column(db.Integer, db.ForeignKey("user"), primary_key=True, nullable=False, index=True)
    original_book_id = db.Column(db.Integer, db.ForeignKey("original_book"), primary_key=True, nullable=False, index=True)
    grade = db.Column(db.Integer, nullable=False)



class CustomBook(db.Model):
    """
    Книга приобретённая пользователем, с возможностью кастомизации
    Содержит ссылку на книгу и кастомизируемые поля
    Если такие поля == NULL, то вместо них следует использовать поля из таблицы Book
    """
    __tablename__ = "сustom_book"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book"), nullable=False, index=True)
    title = db.Column(db.Text())
    cover_id = db.Column(db.Integer, db.ForeignKey("file"), index=True)
    # count = db.Column(db.Integer, nullable=False)  # Подсчёт ссылок
    #    в случае, если мы будем автоматически удалять неиспользуемую кастомизацию


class UserСustomBook(db.Model):
    """
    Сводная таблица пользователя и книги пользователя
    У многих пользователей может быть одинаковая кастомная книга
    Если кто-то изменит книгу, в таблице следует появиться новой
    """
    __tablename__ = "user_сustom_book"

    user_id = db.Column(db.Integer, db.ForeignKey("user"), primary_key=True, nullable=False, index=True)
    custom_book_id = db.Column(db.Integer, db.ForeignKey("сustom_book"), primary_key=True, nullable=False, index=True)
    # У нас есть 2 сценария связи пользователя с книгой:
    # 1.  Пользователь имеет доступ только к кастомной версии
    #       тогда в случае если пользователь кастомизации не делал
    #       нам необходимо сделать нулевую кастомизацию за него
    #       (СustomBook со всеми полями == NULL, кроме поля book_id)
    # 2.  Пользователь имеет доступ ещё и к книгам издания
    #       нам не прийдётся создавать нулевую кастомизацию
    #       нам прийдётся добавить поле is_custom = db.Column(db.Boolean)
    #       тогда поле custom_book_id будет ссылатся на 
    #       CustomBook или Book в зависимости от is_custom
    #       (custom_book_id: db.ForeignKey("сustom_book") | db.ForeignKey("book"))
    #       Когда пользователь создаёт кастомизацию, в db добавляется CustomBook
    #       и custom_book_id переключается на неё, is_custom = True
    #       и если до этого is_custom == True, то мы удаляем старую CustomBook, если её больше ни кто не использует
    #       именно при этом сценарии нам понадобится поле count в CustomBook
    #       поле custom_book_id можно переименовать в book_id
    count_copy = db.Column(db.Integer) # количество копий (возможностей поделится)
                                 # если == NULL: неограниченный терраж, с возможностью распространения
                                 # если == 0: автоудаление



class Group(db.Model):
    __tablename__ = "group"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    name = db.Column(db.String(31))
    ...


class UserGroup(db.Model):
    __tablename__ = "user_group"

    user_id = db.Column(db.Integer, db.ForeignKey("user"), primary_key=True, nullable=False, index=True)
    group_id = db.Column(db.Integer, db.ForeignKey("group"), primary_key=True, nullable=False, index=True)
    # right = db.Column(db.Integer, nullable=False) | db.Column(Enum, nullable=False)
    #   права пользователя в группе, это или число (0 - создатель группы, чем больше число, тем меньше прав)
    #   или перечисление (например: owner, admin, member), не столь гибкое но более наглядное


# В случае, если мы хотим создать чат в вгруппе
class Message(db.Model):
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("user"), nullable=False, index=True)
    group_id = db.Column(db.Integer, db.ForeignKey("group"), index=True)
    # send_id = db.Column(db.Integer, db.ForeignKey("user_group"), nullable=False)
    # Возможно лучше будет сделать ссылку на отношение UserGroup, а не User и Group по отдельности
    # вместо отдельных полей sender group
    send_time = db.Column(db.DateTime, nullable=False, index=True)
    text = db.Column(db.Text())
    answer = db.Column(db.Integer, db.ForeignKey("message"), index=True) # Если нужны ответы на сообщения
    is_pinned = db.Column(db.Boolean)                     # Если нужны закреплённые сообщения



class BookDistribution(db.Model):
    __tablename__ = "book_distribution"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)

    # Здесь информация и об распрстранителе и о распростроняемой книге,
    # в не зависимости от того какой сценарий связи книги и пользователя мы выбрали
    send_id = db.Column(db.Integer, db.ForeignKey("user_сustom_book"), nullable=False, index=True)

    group_id = db.Column(db.Integer, db.ForeignKey("group"), index=True) # Глобальное распространение если == NULL
    # right = db.Column(db.Integer) | db.Column(Enum, nullable=False)    # == NULL, если group_id == NULL
    # права распространеия в группе, вы не можите воспользоватся этим распространением, если у вас не достаточно прав
    # is_invisible = Colum(db.Boolean, default=False) # у кого не достаточно прав, даже не смогут его увидеть

    distribution_date = db.Column(db.Date, nullable=False, index=True)
    count_copy = db.Column(db.Integer) # количество копий (возможностей скачать)
                                 # если == NULL: неограниченный терраж, с возможностью распространения
                                 # если == 0: можно сделать автоудаление
    price = db.Column(db.Numeric, nullable=False, default=0)
    # цена за копию или за весь тирраж, если count_copy == NULL


class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    buyer = db.Column(db.Integer, db.ForeignKey("user"), nullable=False, index=True)
    salesman = db.Column(db.Integer, db.ForeignKey("user"), nullable=False, index=True)
    time = db.Column(db.DateTime, nullable=False, index=True)
    count_copy = db.Column(db.Integer)
    price = db.Column(db.Numeric, nullable=False, default=0)  # общая цена
    book_id = db.Column(db.Integer, db.ForeignKey("сustom_book"), nullable=False, index=True)
    # Если книга учавствовала в транзакции, то если у неё есть счётчик ссылок с автоудалением,
    # то этот счётчик увеличится на 1, и уменьшится на 1 при удалении транзакции
    # => кастомная книга не будет удалена, пока не удалится транзакция,
    # даже если eё больше не будут использовать