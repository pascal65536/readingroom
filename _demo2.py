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
    category_delete,)
from settings import cridentials
from flask_wtf import FlaskForm
from types import SimpleNamespace
from forms import AuthorForm, BookForm, CategoryForm, UploadForm
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.secret_key = os.urandom(256)


# Вспомогательная функция для загрузки файлов с сервера
def download_file(url: str, destination: str):
    import requests
    response = requests.get(url)
    with open(destination, 'wb') as f:
        f.write(response.content)
        

class AuthorManager:
    def __init__(self, app):
        self.app = app
        self.app.add_url_rule("/authors/", "authors", self.authors, methods=["GET"])
        self.app.add_url_rule("/author/create", "create_author", self.create_author, methods=["GET", "POST"])
        self.app.add_url_rule("/author/<string:author_id>/edit", "edit_author", self.edit_author, methods=["GET", "POST"])
        self.app.add_url_rule("/author/delete", "delete_author", self.delete_author, methods=["POST"])

    def authors(self):
        access_token_dct = get_access_token(*cridentials)
        access_token = access_token_dct.get("access_token")
        authors = authors_get(access_token, govdatahub=cridentials[2])
        return render_template("authors_lst.html", authors=authors)

    def create_author(self):
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

    def edit_author(self, author_id):
        access_token_dct = get_access_token(*cridentials)
        access_token = access_token_dct.get("access_token")
        author_dict = author_get(author_id, access_token, govdatahub=cridentials[2])
        author = SimpleNamespace(**author_dict)
        form = AuthorForm(obj=author)
        if request.method == "POST" and form.validate_on_submit():
            json_data = {"name": form.name.data, "name_eng": form.name_eng.data}
            author_put(author_id, json_data, access_token, govdatahub=cridentials[2])
            return redirect(url_for("authors"))
        return render_template("author_form.html", form=form, author=author)

    def delete_author(self):
        author_id = request.form.get("author_id")
        if request.method == "POST" and author_id:
            access_token_dct = get_access_token(*cridentials)
            access_token = access_token_dct.get("access_token")
            author_delete(author_id, access_token, govdatahub=cridentials[2])
        return redirect(url_for("authors"))


class CategoryManager:
    def __init__(self, app):
        self.app = app
        self.app.add_url_rule("/categories/", "categories", self.categories, methods=["GET"])
        self.app.add_url_rule("/category/create", "create_category", self.create_category, methods=["GET", "POST"])
        self.app.add_url_rule("/category/<string:category_id>/edit", "edit_category", self.edit_category, methods=["GET", "POST"])
        self.app.add_url_rule("/category/delete", "delete_category", self.delete_category, methods=["POST"])

    def categories(self):
        access_token_dct = get_access_token(*cridentials)
        access_token = access_token_dct.get("access_token")
        categories = categories_get(access_token, govdatahub=cridentials[2])
        return render_template("categories_lst.html", categories=categories)

    def create_category(self):
        form = CategoryForm()
        if request.method == "POST" and form.validate_on_submit():
            name = form.name.data
            access_token_dct = get_access_token(*cridentials)
            access_token = access_token_dct.get("access_token")
            json_data = {"name": name}
            category_post(json_data, access_token, govdatahub=cridentials[2])
            return redirect(url_for("categories"))
        return render_template("category_form.html", form=form)

    def edit_category(self, category_id):
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

    def delete_category(self):
        category_id = request.form.get("category_id")
        if request.method == "POST" and category_id:
            access_token_dct = get_access_token(*cridentials)
            access_token = access_token_dct.get("access_token")
            category_delete(category_id, access_token, govdatahub=cridentials[2])
        return redirect(url_for("categories"))


# Инициализация менеджеров
# book_manager = BookManager(app)
author_manager = AuthorManager(app)
category_manager = CategoryManager(app)



@app.route("/")
def index():
    access_token_dct = get_access_token(*cridentials)
    access_token = access_token_dct.get("access_token")
    
    # Получаем данные для главной страницы
    books = books_get(access_token, govdatahub=cridentials[2])
    authors = authors_get(access_token, govdatahub=cridentials[2])
    categories = categories_get(access_token, govdatahub=cridentials[2])
    
    return render_template("index.html", books=books, authors=authors, categories=categories)

    

if __name__ == "__main__":
    app.run(debug=True)
