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
