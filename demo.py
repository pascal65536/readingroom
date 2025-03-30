from flask import Flask, render_template, request, redirect, url_for, flash
from utils import (
    book_get,
    get_access_token,
    books_get,
    author_post,
    author_put,
    authors_get,
    authors_delete,
    author_get,
)
from settings import cridentials
import os
from flask_wtf import FlaskForm
from forms import AuthorForm
from types import SimpleNamespace


app = Flask(__name__)
app.secret_key = os.urandom(256)


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
    categories = authors_get(access_token, govdatahub=cridentials[2])
    return render_template("categories_lst.html", categories=books)


@app.route("/book/<string:book_id>")
def book(book_id):
    access_token_dct = get_access_token(*cridentials)
    access_token = access_token_dct.get("access_token")
    book = book_get(book_id, access_token, govdatahub=cridentials[2])
    return render_template("book.html", book=book)


@app.route("/author/create", methods=["GET", "POST"])
def create_book():
    pass
@app.route("/author/create", methods=["GET", "POST"])
def edit_book():
    pass
@app.route("/author/create", methods=["GET", "POST"])
def delete_book():
    pass




@app.route("/author/create", methods=["GET", "POST"])
def create_author():
    form = AuthorForm()
    if request.method == "POST" and form.validate_on_submit():
        name = form.name.data
        name_eng = form.name_eng.data
        access_token_dct = get_access_token(*cridentials)
        access_token = access_token_dct.get("access_token")
        json_data = {"name": name, "name_eng": name_eng}
        response = author_post(json_data, access_token, govdatahub=cridentials[2])
        return redirect(url_for("authors"))
    return render_template("author_form.html", form=form)


@app.route("/author/delete", methods=["POST"])
def delete_author():
    author_id = request.form.get("author_id")
    if request.method == "POST" and author_id:
        access_token_dct = get_access_token(*cridentials)
        access_token = access_token_dct.get("access_token")
        response = authors_delete(author_id, access_token, govdatahub=cridentials[2])
    return redirect(url_for("authors"))


@app.route("/author/<string:author_id>/edit", methods=["GET", "POST"])
def edit_author(author_id):
    print(author_id)
    access_token_dct = get_access_token(*cridentials)
    access_token = access_token_dct.get("access_token")
    # Получение текущего автора
    author_dict = author_get(author_id, access_token, govdatahub=cridentials[2])
    # Преобразование словаря в объект
    author = SimpleNamespace(**author_dict)
    form = AuthorForm(obj=author)
    if request.method == "POST" and form.validate_on_submit():
        json_data = {"name": form.name.data, "name_eng": form.name_eng.data}
        response = author_put(author_id, json_data, access_token, govdatahub=cridentials[2])
        return redirect(url_for("authors"))
    return render_template("author_form.html", form=form, author=author)


if __name__ == "__main__":
    app.run(debug=True)
