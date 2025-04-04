from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length


class UploadForm(FlaskForm):
    file = FileField("Файл", validators=[DataRequired()])
    submit = SubmitField("Загрузить")


class CategoryForm(FlaskForm):
    name = StringField("Название", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Сохранить")


class BookForm(FlaskForm):
    title = StringField("Название", validators=[DataRequired(), Length(max=200)])
    filename_orig = StringField("Оригинальное имя файла", validators=[DataRequired(), Length(max=100)])
    filename_uid = StringField("Новое имя файла", validators=[DataRequired(), Length(max=40)])
    file_path = StringField("Путь к файлу", validators=[DataRequired(), Length(max=200)])
    isbn = StringField("ISBN")
    publication_date = StringField("Дата издания")
    publisher = StringField("Издатель")
    description = TextAreaField("Описание")
    cover_image = StringField("Обложка")
    telegram_link = StringField("Ссылка на телеграм")
    telegram_file_id = StringField("Ссылка на файл в телеграм")
    submit = SubmitField("Сохранить")


class AuthorForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired(message="Имя обязательно для заполнения."), Length(max=100, message="Имя не должно превышать 100 символов."),],)
    name_eng = StringField("Имя на английском",)
    submit = SubmitField("Сохранить")
