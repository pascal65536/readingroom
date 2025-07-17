from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_from_directory,
)
from utils import (
    get_access_token,
    books_get,
    book_get,
    book_update,
    book_delete,
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
    add_category_to_book,
    remove_category_from_book,
    add_author_to_book,
    remove_author_from_book,
    upload_file,
    book_create,
    download_file,
)
from settings import cridentials
from types import SimpleNamespace
from forms import AuthorForm, BookForm, CategoryForm, UploadForm
from wtforms import SelectField
import requests
import os


app = Flask(__name__)
app.secret_key = os.urandom(256)
os.makedirs("_download", exist_ok=True)


def allowed_file(filename, extensions=set()):
    if "." not in filename:
        return False
    if filename.rsplit(".", 1)[1].lower() not in extensions:
        return False
    return True


@app.route("/_download/<filename>")
def get_image(filename):
    return send_from_directory("_download", filename)


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
    cover_image = book.get("cover_image")
    if cover_image and not os.path.exists(os.path.join("_download", cover_image)):
        download_file(cover_image, cover_image, access_token, govdatahub=cridentials[2])
    return render_template("book.html", book=book)


@app.route("/book/<string:book_id>/delete", methods=["GET", "POST"])
def delete_book(book_id):
    if request.method == "POST":
        access_token_dct = get_access_token(*cridentials)
        access_token = access_token_dct.get("access_token")
        book_delete(book_id, access_token, govdatahub=cridentials[2])
    return redirect(url_for("books"))


@app.route("/book/<string:book_id>/download", methods=["GET", "POST"])
def download_book(book_id):
    if request.method == "POST":
        access_token_dct = get_access_token(*cridentials)
        access_token = access_token_dct.get("access_token")
        book = book_get(book_id, access_token)
        local_name = book["filename_orig"]
        filename = book["filename_uid"]
        download_file(filename, local_name, access_token, govdatahub=cridentials[2])
        return send_from_directory("_download", local_name)
    return redirect(url_for("books"))


@app.route("/book/create", methods=["GET", "POST"])
def create_book():
    cache = "_cache"
    os.makedirs(cache, exist_ok=True)
    form = UploadForm()
    if request.method == "POST" and form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename, {"pdf"}):
            file_path = os.path.join(cache, file.filename)
            file.save(file_path)
            access_token_dct = get_access_token(*cridentials)
            access_token = access_token_dct.get("access_token")
            book_dct = upload_file(file_path, access_token, govdatahub=cridentials[2])
            book_id = book_dct["id"]
            os.remove(file_path)
            book_dct.update({"title": book_dct["filename_orig"]})
            book_create(book_id, book_dct, access_token, govdatahub=cridentials[2])
            return redirect(url_for("book", book_id=book_id))
        else:
            form.file.errors.append("Недопустимое расширение файла.")
    return render_template("book_upload.html", form=form)


@app.route("/book/<string:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id):
    access_token_dct = get_access_token(*cridentials)
    access_token = access_token_dct.get("access_token")
    authors = authors_get(access_token, govdatahub=cridentials[2])
    categories = categories_get(access_token, govdatahub=cridentials[2])
    book_dict = book_get(book_id, access_token, govdatahub=cridentials[2])
    book = SimpleNamespace(**book_dict)
    form = BookForm(obj=book)

    # Добавляем поля authors и categories
    form.authors.choices = [("0", "Выберите автора")] + [
        (author.get("id"), author.get("name")) for author in authors
    ]
    form.categories.choices = [("0", "Выберите категорию")] + [
        (category.get("id"), category.get("name")) for category in categories
    ]

    # Предварительное заполнение выбранных авторов и категорий
    selected_authors = [author.get("id") for author in book.authors]
    selected_categories = [category.get("id") for category in book.categories]
    form.authors.process_data(selected_authors)
    form.categories.process_data(selected_categories)

    if request.method == "POST" and form.validate_on_submit():
        json_data = {
            "title": form.title.data if form.title.data else None,
            "isbn": form.isbn.data if form.isbn.data else None,
            "publication_date": (
                form.publication_date.data if form.publication_date.data else None
            ),
            "publisher": form.publisher.data if form.publisher.data else None,
            "description": form.description.data if form.description.data else None,
            "telegram_link": (
                form.telegram_link.data if form.telegram_link.data else None
            ),
            "telegram_file_id": (
                form.telegram_file_id.data if form.telegram_file_id.data else None
            ),
        }
        ret = book_update(book_id, json_data, access_token, govdatahub=cridentials[2])

        # Обработка категорий
        for category in book.categories:
            remove_category_from_book(
                book_id, category.get("id"), access_token, govdatahub=cridentials[2]
            )
        if form.categories.raw_data and "0" not in form.categories.raw_data:
            for category_id in form.categories.raw_data:
                ret = add_category_to_book(
                    book_id, category_id, access_token, govdatahub=cridentials[2]
                )

        # Обработка авторов
        for author in book.authors:
            remove_author_from_book(
                book_id, author.get("id"), access_token, govdatahub=cridentials[2]
            )
        if form.authors.raw_data and "0" not in form.authors.raw_data:
            for author_id in form.authors.raw_data:
                ret = add_author_to_book(
                    book_id, author_id, access_token, govdatahub=cridentials[2]
                )

        return redirect(url_for("books"))
    return render_template("book_form.html", form=form, book=book)


# cover_book upload_file
@app.route("/book/<string:book_id>/cover", methods=["GET", "POST"])
def cover_book(book_id):
    cache = "_cache"
    os.makedirs(cache, exist_ok=True)
    access_token_dct = get_access_token(*cridentials)
    access_token = access_token_dct.get("access_token")
    book = book_get(book_id, access_token, govdatahub=cridentials[2])
    form = UploadForm()
    if request.method == "POST" and form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename, {"jpg", "png", "jpeg"}):
            file_path = os.path.join(cache, file.filename)
            file.save(file_path)
            access_token_dct = get_access_token(*cridentials)
            access_token = access_token_dct.get("access_token")
            ret = upload_file(file_path, access_token, govdatahub=cridentials[2])
            os.remove(file_path)
            # Обновление книги
            if ret.get("filename_uid"):
                json_data = {"cover_image": ret["filename_uid"]}
                access_token_dct = get_access_token(*cridentials)
                access_token = access_token_dct.get("access_token")
                ret = book_update(
                    book_id, json_data, access_token, govdatahub=cridentials[2]
                )
                return redirect(url_for("book", book_id=book_id))
        else:
            form.file.errors.append("Недопустимое расширение файла.")
    return render_template("file_upload.html", form=form, book=book)


@app.route("/")
def index():
    access_token_dct = get_access_token(*cridentials)
    access_token = access_token_dct.get("access_token")

    # Начальное смещение offset
    # offset = request.args.get('offset', default=0)
    # try: offset = int(offset)
    # except ValueError: offset = 0

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
