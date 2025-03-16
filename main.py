import os
import uuid
import json
import shutil
import hashlib
from extensions import db
from models import Book as BookModel
from flask_restful import Api, Resource
from models import Author as AuthorModel
from models import Category as CategoryModel
from flask import Flask, request, jsonify, send_from_directory
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["DATA_FOLDER"] = "data"
app.config["CACHE_FOLDER"] = "_cache"
app.config["SECRET_KEY"] = os.urandom(256)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.urandom(256)

# Инициализация расширений
db.init_app(app)
jwt = JWTManager(app)

# Создание необходимых папок
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["DATA_FOLDER"], exist_ok=True)
os.makedirs(app.config["CACHE_FOLDER"], exist_ok=True)


# Маршрут для входа (пример)
users = {"user1": {"password": "password1"}, "user2": {"password": "password2"}}


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({"msg": "Необходимо указать логин и пароль"}), 400

    if username not in users or users[username]['password'] != password:
        return jsonify({"msg": "Неверный логин или пароль"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


# Функция для расчета MD5
def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


# Маршрут для корневого URL
@app.route("/")
def index():
    books_list = list()
    for book in AuthorModel.query.all()[:10]:
        books_list.append(book.as_dict())
    return jsonify(books_list)


# Ресурсы для авторов
class AuthorList(Resource):
    def get(self):
        authors = AuthorModel.query.all()
        author_list = list()
        for author in authors:
            author_list.append(author.as_dict())
        return jsonify(author_list)

    @jwt_required()
    def post(self):
        authors = AuthorModel.query.all()
        new_author = request.get_json()
        name = new_author.get("name")
        if not name:
            response = jsonify({"message": "Author`s Name required"})
            response.status_code = 400
            return response
        new_author = {
            "name_eng": new_author.get("name_eng"),
            "name": name,
        }

        with app.app_context():
            author_obj = AuthorModel.query.filter_by(name=name).first()
            if author_obj:
                response = jsonify({"message": "Author`s this Name already exists"})
                response.status_code = 400
                return response
            # Создаем новый объект автор и добавляем его в базу данных
            author_obj = AuthorModel(**new_author)
            try:
                db.session.add(author_obj)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                response = jsonify({"message": "Error adding author"})
                response.status_code = 500
                return response
        
        author_obj = AuthorModel.query.filter_by(name=name).first()
        # Возвращаем данные о добавленном авторе
        response = jsonify(author_obj.as_dict())
        response.status_code = 200
        return response


class Author(Resource):
    def get(self, author_id):
        with app.app_context():
            # Ищем автора по id
            author = AuthorModel.query.filter_by(id=author_id).first()
            if not author:
                response = jsonify({"message": "Author not found"})
                response.status_code = 404
                return response
            # Возвращаем данные автора в формате JSON
            return jsonify(author.as_dict())

    @jwt_required()
    def put(self, author_id):
        with app.app_context():
            # Ищем книгу по id
            author = AuthorModel.query.filter_by(id=author_id).first()
            if not author:
                response = jsonify({"message": "Author not found"})
                response.status_code = 404
                return response
            # Получаем данные для обновления
            updated_data = request.get_json()
            # Обновляем поля книги, если они предоставлены
            author.name = updated_data.get("name", author.name)
            author.name_eng = updated_data.get("name_eng", author.name_eng)
            # Пытаемся зафиксировать изменения в базе данных
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                response = jsonify({"message": "Error updating book"})
                response.status_code = 500
                return response
            # Возвращаем обновленные данные книги
            response = jsonify(author.as_dict())
            response.status_code = 200
            return response

    @jwt_required()
    def delete(self, author_id):
        with app.app_context():
            # Ищем книгу по id
            author = AuthorModel.query.filter_by(id=author_id).first()
            if not author:
                response = jsonify({"message": "Author not found"})
                response.status_code = 404
                return response
            # Удаляем запись из базы данных
            try:
                AuthorModel.query.filter_by(id=author_id).delete()
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                response = jsonify({"message": "Error deleting author"})
                response.status_code = 500
                return response
            # Возвращаем успешное сообщение
            response = jsonify({"message": "Author deleted"})
            response.status_code = 200
            return response


# Ресурсы для категорий
class CategoryList(Resource):
    def get(self):
        categories = load_json(app.config["DATA_FOLDER"], "categories.json")
        return jsonify(categories)

    def post(self):
        categories = load_json(app.config["DATA_FOLDER"], "categories.json")
        new_category = request.get_json()
        new_category["id"] = str(uuid.uuid4())
        categories[new_category["id"]] = new_category
        save_json(app.config["DATA_FOLDER"], "categories.json", categories)
        response = jsonify(new_category)
        response.status_code = 201
        return response


class Category(Resource):
    def get(self, category_id):
        categories = load_json(app.config["DATA_FOLDER"], "categories.json")
        category = categories.get(category_id)
        if not category:
            response = jsonify({"message": "Category not found"})
            response.status_code = 404
            return response
        return jsonify(category)

    def put(self, category_id):
        categories = load_json(app.config["DATA_FOLDER"], "categories.json")
        category = categories.get(category_id)
        if not category:
            response = jsonify({"message": "Category not found"})
            response.status_code = 404
            return response
        updated_data = request.get_json()
        categories[category_id].update(updated_data)
        save_json(app.config["DATA_FOLDER"], "categories.json", categories)
        return jsonify(categories[category_id]), 200

    def delete(self, category_id):
        categories = load_json(app.config["DATA_FOLDER"], "categories.json")
        if category_id not in categories:
            response = jsonify({"message": "Category not found"})
            response.status_code = 404
            return response
        del categories[category_id]
        save_json(app.config["DATA_FOLDER"], "categories.json", categories)
        return jsonify({"message": "Category deleted"}), 200


# Ресурсы для книг
class BookList(Resource):
    def get(self):
        books = BookModel.query.all()
        books_list = list()
        for book in books:
            books_list.append(book.as_dict())
        return jsonify(books_list)


class Book(Resource):
    def get(self, book_id):
        with app.app_context():
            # Ищем книгу по id
            book = BookModel.query.filter_by(id=book_id).first()
            if not book:
                response = jsonify({"message": "Book not found"})
                response.status_code = 404
                return response
            # Возвращаем данные книги в формате JSON
            return jsonify(book.as_dict())

    @jwt_required()
    def put(self, book_id):
        with app.app_context():
            # Ищем книгу по id
            book = BookModel.query.filter_by(id=book_id).first()
            if not book:
                response = jsonify({"message": "Book not found"})
                response.status_code = 404
                return response
            # Получаем данные для обновления
            updated_data = request.get_json()
            # Обновляем поля книги, если они предоставлены
            # book.author_id = updated_data.get("author_id", book.author_id)
            # book.category_id = updated_data.get("category_id", book.category_id)
            book.title = updated_data.get("title", book.title)
            book.isbn = updated_data.get("isbn", book.isbn)
            book.publication_date = updated_data.get(
                "publication_date", book.publication_date
            )
            book.publisher = updated_data.get("publisher", book.publisher)
            book.description = updated_data.get("description", book.description)
            book.cover_image = updated_data.get("cover_image", book.cover_image)
            # Пытаемся зафиксировать изменения в базе данных
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                response = jsonify({"message": "Error updating book"})
                response.status_code = 500
                return response
            # Возвращаем обновленные данные книги
            response = jsonify(book.as_dict())
            response.status_code = 200
            return response

    @jwt_required()
    def delete(self, book_id):
        with app.app_context():
            # Ищем книгу по id
            book = BookModel.query.filter_by(id=book_id).first()
            if not book:
                response = jsonify({"message": "Book not found"})
                response.status_code = 404
                return response
            # Удаляем файл, если он существует
            file_path = book.file_path
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except OSError as e:
                    response = jsonify({"message": "Error deleting file"})
                    response.status_code = 500
                    return response
            # Удаляем запись из базы данных
            try:
                BookModel.query.filter_by(id=book_id).delete()
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                response = jsonify({"message": "Error deleting book"})
                response.status_code = 500
                return response
            # Возвращаем успешное сообщение
            response = jsonify({"message": "Book deleted"})
            response.status_code = 200
            return response


# Ресурсы для загрузки файлов
class FileUpload(Resource):
    @jwt_required()
    def post(self):
        # Проверяем наличие файла в запросе
        if "file" not in request.files:
            response = jsonify({"message": "No file part"})
            response.status_code = 400
            return response
        file = request.files["file"]
        # Проверяем, выбран ли файл
        if file.filename == "":
            response = jsonify({"message": "No selected file"})
            response.status_code = 400
            return response
        # Получаем данные о книге из формы
        new_book = request.form.get("json_data")
        if not new_book:
            response = jsonify({"message": "No book data provided"})
            response.status_code = 400
            return response
        try:
            # Парсим данные о книге из JSON
            new_book = json.loads(new_book)
        except json.JSONDecodeError:
            response = jsonify({"message": "Invalid JSON data"})
            response.status_code = 400
            return response
        # Проверяем тип файла
        ext = file.filename.rsplit(".", 1)[-1].lower()
        if ext not in {"pdf", "epub", "mobi"}:
            response = jsonify({"message": "File type not allowed"})
            response.status_code = 400
            return response
        # Генерируем уникальный идентификатор и создаем путь для временного хранения
        uid = str(uuid.uuid4())
        new_filename = f"{uid}.{ext}"
        cache_path = os.path.join(app.config["CACHE_FOLDER"], new_filename)
        file.save(cache_path)
        file_hash = calculate_md5(cache_path)
        uid02 = file_hash[:2]
        uid24 = file_hash[2:4]
        folder_path = os.path.join(app.config["UPLOAD_FOLDER"], uid02, uid24)
        os.makedirs(folder_path, exist_ok=True)
        uid_filename = f"{file_hash}.{ext}"
        file_path = os.path.join(folder_path, uid_filename)
        shutil.move(cache_path, file_path)
        # Обновляем данные о книге с информацией о файле
        new_book.update(
            {
                "id": file_hash,
                "filename_orig": file.filename,
                "filename_uid": uid_filename,
                "file_path": file_path,
            }
        )
        # Проверяем, существует ли уже книга с таким хешем
        with app.app_context():
            book_obj = BookModel.query.filter_by(id=file_hash).first()
            if book_obj:
                response = jsonify(book_obj.as_dict())
                response.status_code = 200
                return response                
            # Создаем новый объект книги и добавляем его в базу данных
            book_obj = BookModel(**new_book)
            try:
                db.session.add(book_obj)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                response = jsonify({"message": "Error adding book"})
                response.status_code = 500
                return response
        # Возвращаем данные о добавленной книге
        response = jsonify(new_book)
        response.status_code = 200
        return response


class FileDownload(Resource):
    @jwt_required()
    def get(self, book_id):
        with app.app_context():
            # Ищем книгу по id
            book = BookModel.query.filter_by(id=book_id).first()
            if not book:
                response = jsonify({"message": "Book not found"})
                response.status_code = 404
                return response

            if not os.path.exists(book.file_path):
                response = jsonify({"message": "File not found on server"})
                response.status_code = 404
                return response

            # Создаем ответ с файлом и устанавливаем заголовок Content-Disposition
            return send_from_directory(
                os.path.dirname(book.file_path),
                os.path.basename(book.file_path),
                as_attachment=True,
            )



class BookCategories(Resource):
    @jwt_required()
    def get(self, book_id):
        with app.app_context():
            book = BookModel.query.filter_by(id=book_id).first()
            if not book:
                return jsonify({"message": "Book not found"}), 404

            categories = book.categories
            return jsonify([category.as_dict() for category in categories]), 200

    @jwt_required()
    def post(self, book_id):
        with app.app_context():
            book = BookModel.query.filter_by(id=book_id).first()
            if not book:
                return jsonify({"message": "Book not found"}), 404

            category_data = request.get_json()
            category_id = category_data.get("category_id")
            if not category_id:
                return jsonify({"message": "Category ID is required"}), 400

            category = CategoryModel.query.filter_by(id=category_id).first()
            if not category:
                return jsonify({"message": "Category not found"}), 404

            if category in book.categories:
                return jsonify({"message": "Category already added to the book"}), 400

            book.categories.append(category)
            db.session.commit()
            return jsonify({"message": "Category added to the book"}), 200

    @jwt_required()
    def delete(self, book_id):
        with app.app_context():
            book = BookModel.query.filter_by(id=book_id).first()
            if not book:
                return jsonify({"message": "Book not found"}), 404

            category_data = request.get_json()
            category_id = category_data.get("category_id")
            if not category_id:
                return jsonify({"message": "Category ID is required"}), 400

            category = CategoryModel.query.filter_by(id=category_id).first()
            if not category:
                return jsonify({"message": "Category not found"}), 404

            if category not in book.categories:
                return jsonify({"message": "Category not found in the book"}), 400

            book.categories.remove(category)
            db.session.commit()
            return jsonify({"message": "Category removed from the book"}), 200


class BookAuthors(Resource):
    @jwt_required()
    def get(self, book_id):
        with app.app_context():
            book = BookModel.query.filter_by(id=book_id).first()
            if not book:
                return jsonify({"message": "Book not found"}), 404

            authors = book.authors
            return jsonify([author.as_dict() for author in authors]), 200

    @jwt_required()
    def post(self, book_id):
        with app.app_context():
            book = BookModel.query.filter_by(id=book_id).first()
            if not book:
                return jsonify({"message": "Book not found"}), 404

            author_data = request.get_json()
            author_id = author_data.get("author_id")
            if not author_id:
                return jsonify({"message": "Author ID is required"}), 400

            author = AuthorModel.query.filter_by(id=author_id).first()
            if not author:
                return jsonify({"message": "Author not found"}), 404

            if author in book.authors:
                return jsonify({"message": "Author already added to the book"}), 400

            book.authors.append(author)
            db.session.commit()
            return jsonify({"message": "Author added to the book"}), 200

    @jwt_required()
    def delete(self, book_id):
        with app.app_context():
            book = BookModel.query.filter_by(id=book_id).first()
            if not book:
                return jsonify({"message": "Book not found"}), 404

            author_data = request.get_json()
            author_id = author_data.get("author_id")
            if not author_id:
                return jsonify({"message": "Author ID is required"}), 400

            author = AuthorModel.query.filter_by(id=author_id).first()
            if not author:
                return jsonify({"message": "Author not found"}), 404

            if author not in book.authors:
                return jsonify({"message": "Author not found in the book"}), 400

            book.authors.remove(author)
            db.session.commit()
            return jsonify({"message": "Author removed from the book"}), 200


# Добавление ресурсов в API
api = Api(app)
api.add_resource(BookList, "/books")
api.add_resource(Book, "/books/<string:book_id>")
api.add_resource(AuthorList, "/authors")
api.add_resource(Author, "/authors/<string:author_id>")
api.add_resource(CategoryList, "/categories")
api.add_resource(Category, "/categories/<string:category_id>")
api.add_resource(FileUpload, "/upload")
api.add_resource(FileDownload, "/download/<string:book_id>")

api.add_resource(BookAuthors, "/books/<string:book_id>/authors")
api.add_resource(BookCategories, "/books/<string:book_id>/categories")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
