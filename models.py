from extensions import db


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    name_eng = db.Column(db.String(100), nullable=True)
    # birth_date = db.Column(db.String(20), nullable=True)
    # biography = db.Column(db.Text, nullable=True)
    books = db.relationship('Book', secondary='book_authors', back_populates='authors')

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "name_eng": self.name_eng,
        }


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship('Book', secondary='book_categories', back_populates='categories')

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class Book(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    filename_orig = db.Column(db.String(100), nullable=True)
    filename_uid = db.Column(db.String(40), nullable=True)
    file_path = db.Column(db.String(200), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    isbn = db.Column(db.String(50), unique=True, nullable=True)
    publication_date = db.Column(db.String(20), nullable=True)
    publisher = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)
    cover_image = db.Column(db.String(200), nullable=True)
    telegram_link = db.Column(db.String(200), nullable=True)
    telegram_file_id = db.Column(db.String(200), nullable=True)
    authors = db.relationship('Author', secondary='book_authors', back_populates='books')
    categories = db.relationship('Category', secondary='book_categories', back_populates='books')

    def as_dict(self):
        return {
            "id": self.id,
            "filename_orig": self.filename_orig,
            "filename_uid": self.filename_uid,
            "file_path": self.file_path,
            "title": self.title,
            "isbn": self.isbn,
            "publication_date": self.publication_date,
            "publisher": self.publisher,
            "description": self.description,
            "cover_image": self.cover_image,
            "telegram_link": self.telegram_link,
            "telegram_file_id": self.telegram_file_id,
            "authors": [author.as_dict() for author in self.authors],
            "categories": [category.as_dict() for category in self.categories],            
        }

# Таблица для связи Book и Author
book_authors = db.Table('book_authors',
    db.Column('book_id', db.String(32), db.ForeignKey('book.id'), primary_key=True),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'), primary_key=True)
)

# Таблица для связи Book и Category
book_categories = db.Table('book_categories',
    db.Column('book_id', db.String(32), db.ForeignKey('book.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

