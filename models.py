from extensions import db


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    name_eng = db.Column(db.String(100), nullable=True)
    books = db.relationship("Book", backref="author", lazy=True)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "name_eng": self.name_eng,
        }


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship("Book", backref="category", lazy=True)

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
    isbn = db.Column(db.String(20), unique=True, nullable=True)
    publication_date = db.Column(db.String(20), nullable=True)
    publisher = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)
    cover_image = db.Column(db.String(200), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=True)

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
            "author_id": self.author_id,
            "category_id": self.category_id,
        }
