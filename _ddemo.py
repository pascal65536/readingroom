
class BookManager:
    def __init__(self, app, upload_folder='uploads'):
        self.app = app
        self.upload_folder = upload_folder
        os.makedirs(upload_folder, exist_ok=True)

        # Добавление маршрутов
        self.app.add_url_rule("/books/", "books", self.books, methods=["GET"])
        self.app.add_url_rule("/book/<string:book_id>", "book", self.book, methods=["GET"])
        self.app.add_url_rule("/book/create", "create_book", self.create_book, methods=["GET", "POST"])
        self.app.add_url_rule("/book/<string:book_id>/edit", "edit_book", self.edit_book, methods=["GET", "POST"])
        self.app.add_url_rule("/book/<string:book_id>/delete", "delete_book", self.delete_book, methods=["POST"])

    def books(self):
        access_token_dct = get_access_token(*cridentials)
        access_token = access_token_dct.get("access_token")
        books = books_get(access_token, govdatahub=cridentials[2])
        return render_template("books_lst.html", books=books)

    def book(self, book_id):
        access_token_dct = get_access_token(*cridentials)
        access_token = access_token_dct.get("access_token")
        book = book_get(book_id, access_token, govdatahub=cridentials[2])
        return render_template("book.html", book=book)

    def create_book(self):
        form = UploadForm()
        if request.method == "POST" and form.validate_on_submit():
            file = form.file.data
            if file and self.allowed_file(file.filename):
                file_path = os.path.join(self.upload_folder, secure_filename(file.filename))
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

    def edit_book(self, book_id):
        access_token_dct = get_access_token(*cridentials)
        access_token = access_token_dct.get("access_token")
        book_dict = book_get(book_id, access_token, govdatahub=cridentials[2])
        form = BookForm(obj=SimpleNamespace(**book_dict))

        if request.method == "POST" and form.validate_on_submit():
            json_data = {
                "title": form.title.data,
                "isbn": form.isbn.data,
                "publication_date": form.publication_date.data,
                "publisher": form.publisher.data,
                "description": form.description.data,
            }

            # Обработка обложки
            cover_image = form.cover_image.data
            if cover_image:
                filename = f"cover_{book_id}.{secure_filename(cover_image.filename).split('.')[-1]}"
                cover_path = os.path.join(self.upload_folder, filename)
                cover_image.save(cover_path)
                json_data["cover_image"] = cover_path

            response = book_update(book_id, json_data, access_token)
            return redirect(url_for("book", book_id=book_id))
            
        return render_template("book_form.html", form=form)

    def delete_book(self, book_id):
        if request.method == "POST":
            access_token_dct = get_access_token(*cridentials)
            access_token = access_token_dct.get("access_token")
            book_delete(book_id, access_token)
        return redirect(url_for("books"))

    def allowed_file(self, filename):
        allowed_extensions = {'pdf'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


class BookManager:
    def __init__(self, app, upload_folder='uploads'):
        self.app = app
        self.upload_folder = upload_folder
        os.makedirs(upload_folder, exist_ok=True)

        # Добавление маршрутов
        self.app.add_url_rule("/books/", "books", self.books, methods=["GET"])
        self.app.add_url_rule("/book/<string:book_id>", "book", self.book, methods=["GET"])
        self.app.add_url_rule("/book/create", "create_book", self.create_book, methods=["GET", "POST"])
        self.app.add_url_rule("/book/<string:book_id>/edit", "edit_book", self.edit_book, methods=["GET", "POST"])
        self.app.add_url_rule("/book/<string:book_id>/delete", "delete_book", self.delete_book, methods=["POST"])

    def books(self):
        access_token_dct = get_access_token(*cridentials)
        access_token = access_token_dct.get("access_token")
        books = books_get(access_token, govdatahub=cridentials[2])
        return render_template("books_lst.html", books=books)

    def book(self, book_id):
        access_token_dct = get_access_token(*cridentials)
        access_token = access_token_dct.get("access_token")
        book = book_get(book_id, access_token, govdatahub=cridentials[2])
        return render_template("book.html", book=book)

    def create_book(self):
        form = UploadForm()
        if request.method == "POST" and form.validate_on_submit():
            file = form.file.data
            if file and self.allowed_file(file.filename):
                file_path = os.path.join(self.upload_folder, secure_filename(file.filename))
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

    def edit_book(self, book_id):
        access_token_dct = get_access_token(*cridentials)
        access_token = access_token_dct.get("access_token")
        book_dict = book_get(book_id, access_token, govdatahub=cridentials[2])
        form = BookForm(obj=SimpleNamespace(**book_dict))

        if request.method == "POST" and form.validate_on_submit():
            json_data = {
                "title": form.title.data,
                "isbn": form.isbn.data,
                "publication_date": form.publication_date.data,
                "publisher": form.publisher.data,
                "description": form.description.data,
            }

            # Обработка обложки
            cover_image = form.cover_image.data
            if cover_image:
                filename = f"cover_{book_id}.{secure_filename(cover_image.filename).split('.')[-1]}"
                cover_path = os.path.join(self.upload_folder, filename)
                cover_image.save(cover_path)
                json_data["cover_image"] = cover_path

            response = book_update(book_id, json_data, access_token)
            return redirect(url_for("book", book_id=book_id))
            
        return render_template("book_form.html", form=form)

    def delete_book(self, book_id):
        if request.method == "POST":
            access_token_dct = get_access_token(*cridentials)
            access_token = access_token_dct.get("access_token")
            book_delete(book_id, access_token)
        return redirect(url_for("books"))

    def allowed_file(self, filename):
        allowed_extensions = {'pdf'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


class BookManager:
    def __init__(self, app, cache_folder='_cache'):
        self.app = app
        self.cache_folder = cache_folder
        os.makedirs(cache_folder, exist_ok=True)

        # Добавление маршрутов
        self.app.add_url_rule("/books/", "books", self.books, methods=["GET"])
        self.app.add_url_rule("/book/<string:book_id>", "book", self.book, methods=["GET"])
        self.app.add_url_rule("/book/create", "create_book", self.create_book, methods=["GET", "POST"])
        self.app.add_url_rule("/book/<string:book_id>/edit", "edit_book", self.edit_book, methods=["GET", "POST"])
        self.app.add_url_rule("/book/<string:book_id>/delete", "delete_book", self.delete_book, methods=["POST"])

    def books(self):
        access_token_dct = get_access_token(*cridentials)
        access_token = access_token_dct.get("access_token")
        books = books_get(access_token, govdatahub=cridentials[2])

        # Загрузка обложек для каждой книги в локальный кэш
        for book in books:
            if book.get("cover_image"):
                cover_url = book["cover_image"]
                local_cover_path = os.path.join(self.cache_folder, f"{book['id']}_cover.jpg")
                if not os.path.exists(local_cover_path):
                    download_file(cover_url, local_cover_path)
                book["local_cover"] = local_cover_path

        return render_template("books_lst.html", books=books)

    def book(self, book_id):
        access_token_dct = get_access_token(*cridentials)
        access_token = access_token_dct.get("access_token")
        book = book_get(book_id, access_token, govdatahub=cridentials[2])

        # Загрузка обложки в локальный кэш
        if book.get("cover_image"):
            cover_url = book["cover_image"]
            local_cover_path = os.path.join(self.cache_folder, f"{book_id}_cover.jpg")
            if not os.path.exists(local_cover_path):
                download_file(cover_url, local_cover_path)
            book["local_cover"] = local_cover_path

        return render_template("book.html", book=book)

    def create_book(self):
        form = UploadForm()
        if request.method == "POST" and form.validate_on_submit():
            file = form.file.data
            if file and self.allowed_file(file.filename):
                file_path = os.path.join(self.cache_folder, secure_filename(file.filename))
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

    def edit_book(self, book_id):
        access_token_dct = get_access_token(*cridentials)
        access_token = access_token_dct.get("access_token")
        book_dict = book_get(book_id, access_token, govdatahub=cridentials[2])
        form = BookForm(obj=SimpleNamespace(**book_dict))

        # Загрузка текущей обложки в локальный кэш
        current_cover_path = None
        if book_dict.get("cover_image"):
            cover_url = book_dict["cover_image"]
            current_cover_path = os.path.join(self.cache_folder, f"{book_id}_cover.jpg")
            if not os.path.exists(current_cover_path):
                download_file(cover_url, current_cover_path)

        if request.method == "POST" and form.validate_on_submit():
            json_data = {
                "title": form.title.data,
                "isbn": form.isbn.data,
                "publication_date": form.publication_date.data,
                "publisher": form.publisher.data,
                "description": form.description.data,
            }

            # Удаление текущей обложки (если выбрано пользователем)
            if form.delete_cover.data:
                json_data["cover_image"] = None

            # Загрузка новой обложки (если предоставлена)
            cover_image_file = form.cover_image.data
            if cover_image_file:
                filename = secure_filename(cover_image_file.filename)
                new_cover_path = os.path.join(self.cache_folder, filename)
                cover_image_file.save(new_cover_path)
                json_data["cover_image"] = new_cover_path

            response = book_update(book_id, json_data, access_token)

            # Удаление локального файла новой обложки после отправки на сервер
            if json_data.get("cover_image") and os.path.exists(new_cover_path):
                os.remove(new_cover_path)

            return redirect(url_for("book", book_id=book_id))

        return render_template(
            "book_form.html",
            form=form,
            current_cover=current_cover_path,
        )

    def delete_book(self, book_id):
        if request.method == "POST":
            access_token_dct = get_access_token(*cridentials)
            access_token = access_token_dct.get("access_token")
            book_delete(book_id, access_token)
            
            # Удаление локальной обложки из кэша
            local_cover_path = os.path.join(self.cache_folder, f"{book_id}_cover.jpg")
            if os.path.exists(local_cover_path):
                os.remove(local_cover_path)

        return redirect(url_for("books"))

    def allowed_file(self, filename):
        allowed_extensions = {'pdf'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

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
