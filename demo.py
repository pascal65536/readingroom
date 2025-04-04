from flask import Flask, render_template, request, redirect, url_for, flash
from utils import (
    get_access_token,
    books_get,
    book_get,
    book_update,
    book_delete,
    book_upload,
    authors_get,
    author_post,
    author_put,
    author_delete,
    author_get,
    categories_get,
    category_get,
    category_post,
    category_put,
    category_delete,
    file_upload,
)
from settings import cridentials
from flask_wtf import FlaskForm
from types import SimpleNamespace
from forms import AuthorForm, BookForm, CategoryForm, UploadForm
from werkzeug.utils import secure_filename
import requests
import os


app = Flask(__name__)
app.secret_key = os.urandom(256)



def allowed_file(filename, extensions=set()):
    if "." not in filename:
        return False
    if filename.rsplit(".", 1)[1].lower() not in extensions:
        return False
    return True


# authors
@app.route("/authors/")
def authors():
    access_token_dct = get_access_token(*cridentials)
    access_token = access_token_dct.get("access_token")
    authors = authors_get(access_token, govdatahub=cridentials[2])
    return render_template("authors_lst.html", authors=authors)


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


# categories
@app.route("/categories/")
def categories():
    access_token_dct = get_access_token(*cridentials)
    access_token = access_token_dct.get("access_token")
    categories = categories_get(access_token, govdatahub=cridentials[2])
    return render_template("categories_lst.html", categories=categories)


@app.route("/category/create", methods=["GET", "POST"])
def create_category():
    form = CategoryForm()
    if request.method == "POST" and form.validate_on_submit():
        name = form.name.data
        access_token_dct = get_access_token(*cridentials)
        access_token = access_token_dct.get("access_token")
        json_data = {"name": name}
        category_post(json_data, access_token, govdatahub=cridentials[2])
        return redirect(url_for("categories"))
    return render_template("category_form.html", form=form)


@app.route("/category/delete", methods=["POST"])
def delete_category():
    category_id = request.form.get("category_id")
    if request.method == "POST" and category_id:
        access_token_dct = get_access_token(*cridentials)
        access_token = access_token_dct.get("access_token")
        category_delete(category_id, access_token, govdatahub=cridentials[2])
    return redirect(url_for("categories"))


@app.route("/category/<string:category_id>/edit", methods=["GET", "POST"])
def edit_category(category_id):
    access_token_dct = get_access_token(*cridentials)
    access_token = access_token_dct.get("access_token")
    category_dict = category_get(category_id, access_token, govdatahub=cridentials[2])
    category = SimpleNamespace(**category_dict)
    form = CategoryForm(obj=category)
    if request.method == "POST" and form.validate_on_submit():
        json_data = {"name": form.name.data}
        category_put(category_id, json_data, access_token, govdatahub=cridentials[2])
        return redirect(url_for("categories"))
    return render_template("category_form.html", form=form, category=category)



# books
@app.route("/books/")
def books():
    access_token_dct = get_access_token(*cridentials)
    access_token = access_token_dct.get("access_token")
    books = books_get(access_token, govdatahub=cridentials[2])
    return render_template("books_lst.html", books=books)

@app.route("/book/<string:book_id>")
def book(book_id):
    access_token_dct = get_access_token(*cridentials)
    access_token = access_token_dct.get("access_token")
    book = book_get(book_id, access_token, govdatahub=cridentials[2])
    return render_template("book.html", book=book)

@app.route("/book/<string:book_id>/delete", methods=["GET", "POST"])
def delete_book(book_id):
    if request.method == "POST":
        access_token_dct = get_access_token(*cridentials)
        access_token = access_token_dct.get("access_token")
        book_delete(book_id, access_token, govdatahub=cridentials[2])
    return redirect(url_for("books"))

@app.route("/book/create", methods=["GET", "POST"])
def create_book():
    cache = '_cache'
    os.makedirs(cache, exist_ok=True)
    form = UploadForm()
    if request.method == "POST" and form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename, {'pdf'}):
            file_path = os.path.join(cache, file.filename)
            file.save(file_path)
            access_token_dct = get_access_token(*cridentials)
            access_token = access_token_dct.get("access_token")
            ret = book_upload(file_path, access_token, govdatahub=cridentials[2])
            book_id = ret["id"]
            os.remove(file_path)
            return redirect(url_for("book", book_id=book_id))
        else:
            form.file.errors.append("Недопустимое расширение файла.")
    return render_template("book_upload.html", form=form)

@app.route("/book/<string:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id):
    access_token_dct = get_access_token(*cridentials)
    access_token = access_token_dct.get("access_token")
    book_dict = book_get(book_id, access_token, govdatahub=cridentials[2])
    book = SimpleNamespace(**book_dict)
    form = BookForm(obj=book)
    if request.method == "POST" and form.validate_on_submit():
        json_data = {
            "title": form.title.data if form.title.data else None,
            "isbn": form.isbn.data if form.isbn.data else None,
            "publication_date": form.publication_date.data if form.publication_date.data else None,
            "publisher": form.publisher.data if form.publisher.data else None,
            "description": form.description.data if form.description.data else None,
            "telegram_link": form.telegram_link.data if form.telegram_link.data else None,
            "telegram_file_id": form.telegram_file_id.data if form.telegram_file_id.data else None,
        }        
        ret = book_update(book_id, json_data, access_token, govdatahub=cridentials[2])
        return redirect(url_for("books"))
    return render_template("book_form.html", form=form, book=book)


# cover_book file_upload
@app.route("/book/<string:book_id>/cover", methods=["GET", "POST"])
def cover_book(book_id):
    cache = '_cache'
    os.makedirs(cache, exist_ok=True)
    access_token_dct = get_access_token(*cridentials)
    access_token = access_token_dct.get("access_token")
    book = book_get(book_id, access_token, govdatahub=cridentials[2])    
    form = UploadForm()
    if request.method == "POST" and form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename, {'jpg', 'png', 'jpeg'}):
            file_path = os.path.join(cache, file.filename)
            file.save(file_path)
            access_token_dct = get_access_token(*cridentials)
            access_token = access_token_dct.get("access_token")
            ret = file_upload(file_path, access_token, govdatahub=cridentials[2])
            os.remove(file_path)
            # Обновление книги
            json_data = {"cover_image": ret["file_path"]} 
            ret = book_update(book_id, json_data, access_token)
            print(ret)
            return redirect(url_for("book", book_id=book_id))
        else:
            form.file.errors.append("Недопустимое расширение файла.")
    return render_template("file_upload.html", form=form, book=book)




@app.route("/")
def index():
    access_token_dct = get_access_token(*cridentials)
    access_token = access_token_dct.get("access_token")
    # Получаем данные для главной страницы
    books = books_get(access_token, govdatahub=cridentials[2])
    authors = authors_get(access_token, govdatahub=cridentials[2])
    categories = categories_get(access_token, govdatahub=cridentials[2])
    return render_template(
        "index.html",
        books=books,
        authors=authors,
        categories=categories,
    )


if __name__ == "__main__":
    app.run(debug=True)
