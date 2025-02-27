import os
import uuid
import json
import hashlib
from flask import Flask, request, jsonify, send_from_directory
from flask_restful import Api, Resource
import logging
import shutil
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


# Настройка логирования
logging.basicConfig(level=logging.DEBUG, filename="main.log")

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["DATA_FOLDER"] = "data"
app.config["CACHE_FOLDER"] = "_cache"
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

# Создание необходимых папок
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["DATA_FOLDER"], exist_ok=True)
os.makedirs(app.config["CACHE_FOLDER"], exist_ok=True)



users = {
    'user1': {'password': 'password1'},
    'user2': {'password': 'password2'}
}

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



def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def load_json(folder_name, file_name):
    filename = os.path.join(folder_name, file_name)
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(dict(), f, ensure_ascii=False, indent=4)
    with open(filename, encoding="utf-8") as f:
        return json.load(f)


def save_json(folder_name, file_name, data):
    filename = os.path.join(folder_name, file_name)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# Ресурсы для авторов
class AuthorList(Resource):
    def get(self):
        authors = load_json(app.config["DATA_FOLDER"], "authors.json")
        return jsonify(authors)

    def post(self):
        authors = load_json(app.config["DATA_FOLDER"], "authors.json")
        new_author = request.get_json()
        for key, author in authors.items():
            if author["name"] == new_author["name"]:
                response = jsonify({"message": "Author with this name already exists"})
                response.status_code = 400
                return response
        new_author["id"] = str(uuid.uuid4())
        authors.setdefault(new_author["id"], new_author)
        save_json(app.config["DATA_FOLDER"], "authors.json", authors)
        response = jsonify(new_author)
        response.status_code = 200
        return response


class Author(Resource):
    def get(self, author_id):
        authors = load_json(app.config["DATA_FOLDER"], "authors.json")
        author = authors.get(author_id)
        if not author:
            response = jsonify({"message": "Author not found"})
            response.status_code = 404
            return response
        return jsonify(author)

    def put(self, author_id):
        authors = load_json(app.config["DATA_FOLDER"], "authors.json")
        author = authors.get(author_id)
        if not author:
            response = jsonify({"message": "Author not found"})
            response.status_code = 404
            return response
        updated_data = request.get_json()
        authors[author_id].update(updated_data)
        save_json(app.config["DATA_FOLDER"], "authors.json", authors)
        response = jsonify(authors[author_id])
        response.status_code = 200
        return response

    def delete(self, author_id):
        authors = load_json(app.config["DATA_FOLDER"], "authors.json")
        if author_id not in authors:
            response = jsonify({"message": "Author not found"})
            response.status_code = 404
            return response
        del authors[author_id]
        save_json(app.config["DATA_FOLDER"], "authors.json", authors)
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
        books = load_json(app.config["DATA_FOLDER"], "books.json")
        return jsonify(books)


class Book(Resource):
    def get(self, book_id):
        books = load_json(app.config["DATA_FOLDER"], "books.json")
        book = books.get(book_id)
        if not book:
            response = jsonify({"message": "Book not found"})
            response.status_code = 404
            return response
        return jsonify(book)

    def put(self, book_id):
        books = load_json(app.config["DATA_FOLDER"], "books.json")
        book = books.get(book_id)
        if not book:
            response = jsonify({"message": "Book not found"})
            response.status_code = 404
            return response           
        updated_data = request.get_json()
        book.update(updated_data)
        save_json(app.config["DATA_FOLDER"], "books.json", books)
        response = jsonify(book)
        response.status_code = 200
        return response

    def delete(self, book_id):
        books = load_json(app.config["DATA_FOLDER"], "books.json")
        book = books.get(book_id)
        if not book:
            response = jsonify({"message": "Book not found"})
            response.status_code = 404
            return response 

        books.pop(book_id)
        save_json(app.config["DATA_FOLDER"], "books.json", books)
        file_path = book.get("file_path")
        if file_path and os.path.exists(file_path):
            os.remove(file_path)            

        response = jsonify({"message": "Book deleted"})
        response.status_code = 200
        return response 


# Ресурсы для загрузки файлов
class FileUpload(Resource):
    def post(self):
        if "file" not in request.files:
            response = jsonify({"message": "No file part"})
            response.status_code = 400
            return response

        file = request.files["file"]
        if file.filename == "":
            response = jsonify({"message": "No selected file"})
            response.status_code = 400
            return response

        new_book = request.form.get("json_data")
        if not new_book:
            response = jsonify({"message": "No book data provided"})
            response.status_code = 400
            return response

        try:
            new_book = json.loads(new_book)
        except json.JSONDecodeError:
            response = jsonify({"message": "Invalid JSON data"})
            response.status_code = 400
            return response

        ext = file.filename.rsplit(".", 1)[-1].lower()
        if ext not in {"pdf", "epub", "mobi"}:
            response = jsonify({"message": "File type not allowed"})
            response.status_code = 400
            return response

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

        new_book.update(
            {
                "id": file_hash,
                "filename_orig": file.filename,
                "filename_uid": uid_filename,
                "file_path": file_path,
            }
        )

        books = load_json(app.config["DATA_FOLDER"], "books.json")
        if file_hash in books:
            response = jsonify({"message": "A file with this hash already exists"})
            response.status_code = 400
            return response

        books[file_hash] = new_book
        save_json(app.config["DATA_FOLDER"], "books.json", books)
        response = jsonify(new_book)
        response.status_code = 200
        return response


class FileDownload(Resource):
    def get(self, book_id):
        # Загружаем данные о книгах
        books = load_json(app.config["DATA_FOLDER"], "books.json")
        if book_id not in books:
            response = jsonify({"message": "File not found"})
            response.status_code = 404
            return response

        book = books[book_id]
        file_path = book.get("file_path")
        if not os.path.exists(file_path):
            response = jsonify({"message": "File not found on server"})
            response.status_code = 404
            return response

        # Создаем ответ с файлом и устанавливаем заголовок Content-Disposition
        return send_from_directory(
            os.path.dirname(file_path),
            os.path.basename(file_path),
            as_attachment=True,
        )


api = Api(app)
api.add_resource(BookList, "/books")
api.add_resource(Book, "/books/<string:book_id>")
api.add_resource(AuthorList, "/authors")
api.add_resource(Author, "/authors/<string:author_id>")
api.add_resource(CategoryList, "/categories")
api.add_resource(Category, "/categories/<string:category_id>")
api.add_resource(FileUpload, "/upload")
api.add_resource(FileDownload, "/download/<string:book_id>")

if __name__ == "__main__":
    app.run(debug=True)
