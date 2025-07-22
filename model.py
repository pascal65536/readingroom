# Это конечно не точная и не завершённая модель

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import  (
    Column, ForeignKey,
    Boolean, Integer, Float, Numeric,
    String, Text, 
    Date, DateTime
)


class Base(DeclarativeBase): pass


# class File(Base): ...
# class FileHead(Base): ...
# class FileData(Base): ...

# class GeoAddress(Base): ...

# class Author(Base): ...
# class AuthorBook(Base): ...
# class OriginalBook(Base): ...

# class Publisher(Base): ...
# class Book(Base): ...

# class User(Base): ...
# class UserAuthor(Base): ...

# class CustomBook(Base): ...
# class UserCustomBook(Base): ...

# class Group(Base): ...
# class UserGroup(Base): ...
# class Message(Base): ...

# class BookDistribution(Base): ...
# class Transaction(Base): ...



class File(Base):
    __tablename__ = "file"
  
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    head_id = Column(Integer, ForeignKey("file_head"), nullable=False)
    data_id = Column(Integer, ForeignKey("file_data"), nullable=False)


class FileHead(Base):
    """
    Заголовок файла - данные (обычно визуальные), которуе может исменить пользователь
    (это позволяет разным пользователям иметь один файл с разным иминем)
    """
    __tablename__ = "file_head"
  
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    name = Column(String(255))
    ...


class FileData(Base):
    """
    Данные неизменяемые пользователем
    """
    __tablename__ = "file_data"
  
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    path = Column(String(255), unique=True, nullable=False)
    # count = Column(Integer, nullable=False)  # Подсчёт ссылок в случае, если мы будем автоматически удалять неиспользуемый файл



class GeoAddress(Base):
    __tablename__ = "geo_address"
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    country = Column(String(63))
    region = Column(String(63))
    city = Column(String(63))
    street = Column(String(127))
    building = Column(String(20))
    apartment = Column(String(20))
    # Координаты (для карт)
    latitude = Column(Numeric(9, 6))  # Широта: 90.000000
    longitude = Column(Numeric(9, 6)) # Долгота: 180.000000
    # Почтовый индекс
    postal_code = Column(String(16))



class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    name = Column(String(31), nullable=False)
    date_birth = Column(Date, nullable=False)
    date_death = Column(Date)
    address_id = Column(Integer, ForeignKey("geo_address"))



class OriginalBook(Base):
    __tablename__ = "оriginal_book"
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    name = Column(String(255))
    writing_date = Column(Date, nullable=False)
    # Если понадобится оригинальный текст
    # text = Column(Integer, ForeignKey("file"), unique=True) | Column(Integer, Text, unique=True, nullable=False)


class AuthorBook(Base):
    """
    Таблица для связи автора и первоисточника
    У книги можт быть несколько авторов
    """
    __tablename__ = "author-book"
    
    author_id = Column(Integer, ForeignKey("author"), nullable=False)
    оriginal_book_id = Column(Integer, ForeignKey("оriginal_book"), nullable=False)



class Publisher(Base):
    __tablename__ = "publisher"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    name = Column(String(31), nullable=False)
    address_id = Column(Integer, ForeignKey("geo_address"))


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    isbn = Column(String(13), unique=True, nullable=False)
    title = Column(Text())
    original_id = Column(Integer, ForeignKey("оriginal_book"), nullable=False)
    cover_id = Column(Integer, ForeignKey("file"))
    text_id = Column(Integer, ForeignKey("file"), nullable=False)
    publisher_id = Column(Integer, ForeignKey("publisher"))
    publication_date = Column(Date, nullable=False)
    count_copy = Column(Integer, nullable=False) # количество ссылок, может быть полезно для статистики
    grade = Column(Float)



class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    name = Column(String(63))
    login = Column(String(63), nullable=False, unique=True)
    password = Column(String(63), nullable=False)
    avatar = Column(Integer, ForeignKey("file"))
    title = Column(Text())
    email = Column(String(320))
    ...


class CustomBook(Base):
    """
    Книга приобретённая пользователем, с возможностью кастомизации
    Содержит ссылку на книгу и кастомизируемые поля
    Если такие поля == NULL, то вместо них следует использовать поля из таблицы Book
    """
    __tablename__ = "сustom_book"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    book_id = Column(Integer, ForeignKey("book"), nullable=False)
    title = Column(Text())
    cover_id = Column(Integer, ForeignKey("file"))
    # count = Column(Integer, nullable=False)  # Подсчёт ссылок
    #    в случае, если мы будем автоматически удалять неиспользуемую кастомизацию


class UserСustomBook(Base):
    """
    Сводная таблица пользователя и книги пользователя
    У многих пользователей может быть одинаковая кастомная книга
    Если кто-то изменит книгу, в таблице следует появиться новой
    """
    __tablename__ = "user-сustom_book"

    user_id = Column(Integer, ForeignKey("user"), nullable=False)
    custom_book_id = Column(Integer, ForeignKey("сustom_book"), nullable=False)
    # У нас есть 2 сценария связи пользователя с книгой:
    # 1.  Пользователь имеет доступ только к кастомной версии
    #       тогда в случае если пользователь кастомизации не делал
    #       нам необходимо сделать нулевую кастомизацию за него
    #       (СustomBook со всеми полями == NULL, кроме поля book_id)
    # 2.  Пользователь имеет доступ ещё и к книгам издания
    #       нам не прийдётся создавать нулевую кастомизацию
    #       нам прийдётся добавить поле is_custom = Column(Boolean)
    #       тогда поле custom_book_id будет ссылатся на 
    #       CustomBook или Book в зависимости от is_custom
    #       (custom_book_id: ForeignKey("сustom_book") | ForeignKey("book"))
    #       Когда пользователь создаёт кастомизацию, в db добавляется CustomBook
    #       и custom_book_id переключается на неё, is_custom = True
    #       и если до этого is_custom == True, то мы удаляем старую CustomBook, если её больше ни кто не использует
    #       именно при этом сценарии нам понадобится поле count в CustomBook
    #       поле custom_book_id можно переименовать в book_id
    count_copy = Column(Integer) # количество копий (возможностей поделится)
                                 # если == NULL: неограниченный терраж, с возможностью распространения
                                 # если == 0: автоудаление


class UserAuthor(Base):
    """
    Пользователь может быть несколькими авторами (псевдонимы)
    Также, в редких случаях, и несколько пользователей могут быть одним автором
    """
    __tablename__ = "user-author"

    user_id = Column(Integer, ForeignKey("User"), nullable=False)
    author_id = Column(Integer, ForeignKey("Author"), nullable=False)



class Group(Base):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    name = Column(String(31))
    ...


class UserGroup(Base):
    __tablename__ = "user-group"

    user_id = Column(Integer, ForeignKey("user"), nullable=False)
    group_id = Column(Integer, ForeignKey("group"), nullable=False)
    # right = Column(Integer, nullable=False) | Column(Enum, nullable=False)
    #   права пользователя в группе, это или число (0 - создатель группы, чем больше число, тем меньше прав)
    #   или перечисление (например: owner, admin, member), не столь гибкое но более наглядное


# В случае, если мы хотим создать чат в вгруппе
class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    sender_id = Column(Integer, ForeignKey("user"), nullable=False)
    group_id = Column(Integer, ForeignKey("group"), nullable=False)
    # send_id = Column(Integer, ForeignKey("user-group"), nullable=False)
    # Возможно лучше будет сделать ссылку на отношение UserGroup, а не User и Group по отдельности
    # вместо отдельных полей sender group
    send_time = Column(DateTime, nullable=False)
    text = Column(Text())
    answer = Column(Integer, ForeignKey("message")) # Если нужны ответы на сообщения
    is_pinned = Column(Boolean)                     # Если нужны закреплённые сообщения



class BookDistribution(Base):
    __tablename__ = "book_distribution"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)

    # Здесь информация и об распрстранителе и о распростроняемой книге,
    # в не зависимости от того какой сценарий связи книги и пользователя мы выбрали
    send_id = Column(Integer, ForeignKey("user-сustom_book"), nullable=False)

    group_id = Column(Integer, ForeignKey("group"))  # Глобальное распространение если == NULL
    # right = Column(Integer) | Column(Enum, nullable=False)    # == NULL, если group_id == NULL
    # права распространеия в группе, вы не можите воспользоватся этим распространением, если у вас не достаточно прав
    # is_invisible = Colum(Boolean, default=False) # у кого не достаточно прав, даже не смогут его увидеть

    distribution_date = Column(Date, nullable=False)
    count_copy = Column(Integer) # количество копий (возможностей скачать)
                                 # если == NULL: неограниченный терраж, с возможностью распространения
                                 # если == 0: можно сделать автоудаление
    price = Column(Numeric, nullable=False, default=0)
    # цена за копию или за весь тирраж, если count_copy == NULL


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    buyer = Column(Integer, ForeignKey("user"), nullable=False)
    salesman = Column(Integer, ForeignKey("user"), nullable=False)
    time = Column(DateTime, nullable=False)
    count_copy = Column(Integer)
    price = Column(Numeric, nullable=False, default=0)  # общая цена
    book_id = Column(Integer, ForeignKey("сustom_book"), nullable=False)
    # Если книга учавствовала в транзакции, то если у неё есть счётчик ссылок с автоудалением,
    # то этот счётчик увеличится на 1, и уменьшится на 1 при удалении транзакции
    # => кастомная книга не будет удалена, пока не удалится транзакция,
    # даже если eё больше не будут использовать