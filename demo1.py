from flask import Flask, render_template, request, redirect, url_for, flash
from utils import (
    get_access_token,
    book_get,
    books_get,
    book_update,
    book_delete,
    book_upload,
    author_post,
    author_put,
    authors_get,
    authors_delete,
    author_get,
    categories_get,
)
from settings import cridentials
from flask_wtf import FlaskForm
from forms import AuthorForm, BookForm, CategoryForm, UploadForm
from types import SimpleNamespace
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.secret_key = os.urandom(256)


def allowed_file(filename, extensions=set()):
    if "." not in filename:
        return False
    if filename.rsplit(".", 1)[1].lower() not in extensions:
        return False
    return True


@app.route("/")
def index():
    access_token_dct = get_access_token(*cridentials)
    access_token = access_token_dct.get("access_token")
    books = books_get(access_token, govdatahub=cridentials[2])
    return render_template("template.html", books=books)


@app.route("/books/")
def books():
    access_token_dct = get_access_token(*cridentials)
    access_token = access_token_dct.get("access_token")
    books = books_get(access_token, govdatahub=cridentials[2])
    return render_template("books_lst.html", books=books)


@app.route("/authors/")
def authors():
    access_token_dct = get_access_token(*cridentials)
    access_token = access_token_dct.get("access_token")
    authors = authors_get(access_token, govdatahub=cridentials[2])
    return render_template("authors_lst.html", authors=authors)


@app.route("/categories/")
def categories():
    access_token_dct = get_access_token(*cridentials)
    access_token = access_token_dct.get("access_token")
    categories = categories_get(access_token, govdatahub=cridentials[2])
    return render_template("categories_lst.html", categories=categories)


@app.route("/book/<string:book_id>")
def book(book_id):
    access_token_dct = get_access_token(*cridentials)
    access_token = access_token_dct.get("access_token")
    book = book_get(book_id, access_token, govdatahub=cridentials[2])
    return render_template("book.html", book=book)


@app.route("/book/create", methods=["GET", "POST"])
def create_book():
    cache = '_cache'
    os.makedirs(cache, exist_ok=True)
    form = UploadForm()
    if request.method == "POST" and form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename, {'pdf'}):
            # Сохраняем файл в папку "_cache"
            file_path = os.path.join(cache, file.filename)
            file.save(file_path)
            # Получаем токен доступа и загружаем книгу
            access_token_dct = get_access_token(*cridentials)
            access_token = access_token_dct.get("access_token")
            ret = book_upload(file_path, access_token, govdatahub=cridentials[2])
            book_id = ret["id"]
            os.remove(file_path)
            # Перенаправляем на страницу книги
            return redirect(url_for("book", book_id=book_id))
        else:
            form.file.errors.append("Недопустимое расширение файла.")

    return render_template("book_upload.html", form=form)

@app.route("/book/<string:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id):
    cache = '_cache'
    os.makedirs(cache, exist_ok=True)  # Создаем папку _cache, если она не существует

    access_token_dct = get_access_token(*cridentials)
    access_token = access_token_dct.get("access_token")
    
    # Получение текущей книги
    book_dict = book_get(book_id, access_token, govdatahub=cridentials[2])
    # Преобразование словаря в объект
    book = SimpleNamespace(**book_dict)
    form = BookForm(obj=book)

    if request.method == "POST" and form.validate_on_submit():
        json_data = {
            "title": form.title.data,
            "isbn": form.isbn.data,
            "publication_date": form.publication_date.data,
            "publisher": form.publisher.data,
            "description": form.description.data,
            "telegram_link": form.telegram_link.data,
            "telegram_file_id": form.telegram_file_id.data,
        }

        file_path = None
        cover_image = form.cover_image.data
        if cover_image:
            # Обработка загрузки изображения
            filename = secure_filename(cover_image.filename)
            file_path = os.path.join(cache, filename)
            cover_image.save(file_path)

        # Обновляем данные книги
        response = book_update(book_id, json_data, access_token, govdatahub=cridentials[2], cover_image=file_path)
        print(response)
        
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

        if response.get("message") == "Book not found":
            # Обработка ошибки, если книга не найдена
            return redirect(url_for("books"))
        
        return redirect(url_for("books"))
    
    return render_template("book_form.html", form=form, book=book)

@app.route("/book/<string:book_id>/delete", methods=["GET", "POST"])
def delete_book(book_id):
    if request.method == "POST":
        access_token_dct = get_access_token(*cridentials)
        access_token = access_token_dct.get("access_token")
        book_delete(book_id, access_token, govdatahub=cridentials[2])
    return redirect(url_for("books"))


@app.route("/author/create", methods=["GET", "POST"])
def create_author():
    form = AuthorForm()
    if request.method == "POST" and form.validate_on_submit():
        name = form.name.data
        name_eng = form.name_eng.data
        access_token_dct = get_access_token(*cridentials)
        access_token = access_token_dct.get("access_token")
        json_data = {"name": name, "name_eng": name_eng}
        author_post(json_data, access_token, govdatahub=cridentials[2])
        return redirect(url_for("authors"))
    return render_template("author_form.html", form=form)


@app.route("/author/delete", methods=["POST"])
def delete_author():
    author_id = request.form.get("author_id")
    if request.method == "POST" and author_id:
        access_token_dct = get_access_token(*cridentials)
        access_token = access_token_dct.get("access_token")
        authors_delete(author_id, access_token, govdatahub=cridentials[2])
    return redirect(url_for("authors"))


@app.route("/author/<string:author_id>/edit", methods=["GET", "POST"])
def edit_author(author_id):
    access_token_dct = get_access_token(*cridentials)
    access_token = access_token_dct.get("access_token")
    # Получение текущего автора
    author_dict = author_get(author_id, access_token, govdatahub=cridentials[2])
    # Преобразование словаря в объект
    author = SimpleNamespace(**author_dict)
    form = AuthorForm(obj=author)
    if request.method == "POST" and form.validate_on_submit():
        json_data = {"name": form.name.data, "name_eng": form.name_eng.data}
        author_put(author_id, json_data, access_token, govdatahub=cridentials[2])
        return redirect(url_for("authors"))
    return render_template("author_form.html", form=form, author=author)


if __name__ == "__main__":
    app.run(debug=True)
