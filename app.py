import os

from flask import Flask, render_template
from extensions import db


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def index():
    books = list()
    return render_template("index.html", books=books)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)