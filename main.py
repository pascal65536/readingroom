import os
import uuid
import json
import hashlib
from flask import Flask, request, jsonify, send_from_directory
from flask_restful import Api, Resource
import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, filename='main.log')

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["DATA_FOLDER"] = "data"

# Создание необходимых папок
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["DATA_FOLDER"], exist_ok=True)

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
        new_author['name']
        for key, author in authors.items():
            if author['name'] == new_author['name']:
                response = jsonify({"message": "Author with this name already exists"})
                response.status_code = 400
                return response
        authors.setdefault(str(uuid.uuid4()), new_author)
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
        return jsonify(authors[author_id]), 200

    def delete(self, author_id):
        authors = load_json(app.config["DATA_FOLDER"], "authors.json")
        if author_id not in authors:
            return jsonify({"message": "Author not found"}), 404
        del authors[author_id]
        save_json(app.config["DATA_FOLDER"], "authors.json", authors)
        return jsonify({"message": "Author deleted"}), 200

# Ресурсы для категорий
class CategoryList(Resource):
    def get(self):
        categories = load_json(app.config["DATA_FOLDER"], "categories.json")
        return jsonify(categories)

    def post(self):
        categories = load_json(app.config["DATA_FOLDER"], "categories.json")
        new_category = request.get_json()
        new_category['id'] = str(uuid.uuid4())
        categories[new_category['id']] = new_category
        save_json(app.config["DATA_FOLDER"], "categories.json", categories)
        return jsonify(new_category), 201

class Category(Resource):
    def get(self, category_id):
        categories = load_json(app.config["DATA_FOLDER"], "categories.json")
        category = categories.get(category_id)
        if not category:
            return jsonify({"message": "Category not found"}), 404
        return jsonify(category)

    def put(self, category_id):
        categories = load_json(app.config["DATA_FOLDER"], "categories.json")
        category = categories.get(category_id)
        if not category:
            return jsonify({"message": "Category not found"}), 404
        updated_data = request.get_json()
        categories[category_id].update(updated_data)
        save_json(app.config["DATA_FOLDER"], "categories.json", categories)
        return jsonify(categories[category_id]), 200

    def delete(self, category_id):
        categories = load_json(app.config["DATA_FOLDER"], "categories.json")
        if category_id not in categories:
            return jsonify({"message": "Category not found"}), 404
        del categories[category_id]
        save_json(app.config["DATA_FOLDER"], "categories.json", categories)
        return jsonify({"message": "Category deleted"}), 200

# Ресурсы для книг
class BookList(Resource):
    def get(self):
        books = load_json(app.config["DATA_FOLDER"], "books.json")
        return jsonify(books)

    def post(self):
        if "file" not in request.files:
            return jsonify({"message": "No file part"}), 400
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"message": "No selected file"}), 400

        new_book = request.form.get("json_data")
        if not new_book:
            return jsonify({"message": "No book data provided"}), 400
        try:
            new_book = json.loads(new_book)
        except json.JSONDecodeError:
            return jsonify({"message": "Invalid JSON data"}), 400

        ext = file.filename.rsplit(".", 1)[-1].lower()
        if ext not in {"pdf", "epub", "mobi"}:
            return jsonify({"message": "File type not allowed"}), 400

        uid = str(uuid.uuid4())
        new_filename = f"{uid}.{ext}"
        folder_path = os.path.join(app.config["UPLOAD_FOLDER"], uid[:2], uid[2:4])
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, new_filename)
        file.save(file_path)
        file_hash = calculate_md5(file_path)

        new_book.update({
            "id": uid,
            "filename_orig": file.filename,
            "filename_uid": new_filename,
            "file_path": file_path,
            "file_hash": file_hash
        })

        books = load_json(app.config["DATA_FOLDER"], "books.json")
        books.append(new_book)
        save_json(app.config["DATA_FOLDER"], "books.json", books)
        return jsonify(new_book), 201

class Book(Resource):
    def get(self, book_id):
        books = load_json(app.config["DATA_FOLDER"], "books.json")
        book = next((b for b in books if b["id"] == book_id), None)
        if not book:
            return jsonify({"message": "Book not found"}), 404
        return jsonify(book)

    def put(self, book_id):
        books = load_json(app.config["DATA_FOLDER"], "books.json")
        book = next((b for b in books if b["id"] == book_id), None)
        if not book:
            return jsonify({"message": "Book not found"}), 404
        updated_data = request.get_json()
        book.update(updated_data)
        save_json(app.config["DATA_FOLDER"], "books.json", books)
        return jsonify(book), 200

    def delete(self, book_id):
        books = load_json(app.config["DATA_FOLDER"], "books.json")
        book = next((b for b in books if b["id"] == book_id), None)
        if not book:
            return jsonify({"message": "Book not found"}), 404
        books.remove(book)
        save_json(app.config["DATA_FOLDER"], "books.json", books)
        if os.path.exists(book["file_path"]):
            os.remove(book["file_path"])
        return jsonify({"message": "Book deleted"}), 200


# Ресурсы для загрузки файлов
class FileUpload(Resource):
    def post(self):

        if "file" not in request.files:
            return jsonify({"message": "No file part"}), 400
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"message": "No selected file"}), 400

        ext = file.filename.rsplit(".", 1)[-1].lower()
        if ext not in {"pdf", "epub", "mobi"}:
            return jsonify({"message": "File type not allowed"}), 400

        uid = str(uuid.uuid4())
        new_filename = f"{uid}.{ext}"
        folder_path = os.path.join(app.config["UPLOAD_FOLDER"], uid[:2], uid[2:4])
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, new_filename)
        file.save(file_path)
        file_hash = calculate_md5(file_path)

        new_book = {
            "id": uid,
            "filename_orig": file.filename,
            "filename_uid": new_filename,
            "file_path": file_path,
            "file_hash": file_hash
        }   

        books = load_json(app.config["DATA_FOLDER"], "books.json")
        books.append(new_book)
        save_json(app.config["DATA_FOLDER"], "books.json", books)
        return jsonify(new_book), 200


class FileDownload(Resource):
    def get(self, file_id):
        books = load_json(app.config["DATA_FOLDER"], "books.json")
        book = next((b for b in books if b["id"] == file_id), None)
        if not book:
            return jsonify({"message": "Book not found"}), 404
        return send_from_directory(os.path.dirname(book["file_path"]), book["filename_uid"])


api = Api(app)
api.add_resource(BookList, "/books")
api.add_resource(Book, "/books/<string:book_id>")
api.add_resource(AuthorList, "/authors")
api.add_resource(Author, "/authors/<string:author_id>")
api.add_resource(CategoryList, "/categories")
api.add_resource(Category, "/categories/<string:category_id>")
api.add_resource(FileUpload, "/upload")
api.add_resource(FileDownload, "/download/<string:file_id>")

if __name__ == "__main__":
    app.run(debug=True)

