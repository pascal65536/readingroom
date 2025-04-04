from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FieldList, FormField, BooleanField
from wtforms.validators import DataRequired, Length, URL, Optional
from flask_wtf.file import FileAllowed, FileField, FileRequired


class UploadForm(FlaskForm):
    file = FileField("Файл", validators=[DataRequired()])
    submit = SubmitField("Загрузить")


class CategoryForm(FlaskForm):
    name = StringField("Название", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Сохранить")

class AuthorForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired(message="Имя обязательно для заполнения."), Length(max=100, message="Имя не должно превышать 100 символов."),],)
    name_eng = StringField("Имя на английском",)
    submit = SubmitField("Сохранить")

class BookForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(max=200)])
    isbn = StringField('ISBN', validators=[Length(max=20)])
    publication_date = StringField('Дата публикации', validators=[Length(max=20)])
    publisher = StringField('Издатель', validators=[Length(max=200)])
    telegram_link = StringField('Telegram Link', validators=[Length(max=200)])
    telegram_file_id = StringField('Telegram File ID', validators=[Length(max=200)])
    # authors = StringField('Authors (comma separated)', validators=[Length(max=500)])
    # categories = StringField('Categories (comma separated)', validators=[Length(max=500)])
    description = TextAreaField('Описание')
    # cover_image = FileField('Обложка книги', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Только изображения!')])
    # delete_cover = BooleanField('Удалить текущую обложку')
    submit = SubmitField('Сохранить')
