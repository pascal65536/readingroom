from flask import Flask, render_template
from utils import book_get, get_access_token, books_get
app = Flask(__name__)

@app.route("/")
def index():
    ret = get_access_token("user1", "password1", govdatahub="govdatahub.ru")
    access_token = ret.get("access_token")
    ret = books_get(access_token, govdatahub="govdatahub.ru")
    return render_template("template.html", books=ret)

@app.route("/book/<string:book_id>")
def book(book_id):
    ret = get_access_token("user1", "password1", govdatahub="govdatahub.ru")
    access_token = ret.get("access_token")
    book = book_get(book_id, access_token, govdatahub="govdatahub.ru")
    print(book)
    return render_template("book.html", book=book)


if __name__ == "__main__":
    app.run(debug=True)