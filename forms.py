from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField, FieldList, FormField
from wtforms.validators import DataRequired, Length, URL, Optional


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
    title = StringField("Название", validators=[DataRequired(), Length(max=200)])
    filename_orig = StringField("Оригинальное имя файла", validators=[DataRequired(), Length(max=100)])
    filename_uid = StringField("Новое имя файла", validators=[DataRequired(), Length(max=40)])
    file_path = StringField("Путь к файлу", validators=[DataRequired(), Length(max=200)])
    isbn = StringField("ISBN")
    publication_date = StringField("Дата издания")
    publisher = StringField('Издательство', validators=[Length(max=200)])
    description = TextAreaField("Описание")
    telegram_link = StringField('Ссылка на Telegram', validators=[Optional(), URL()])
    telegram_file_id = StringField('File ID в Telegram')
    cover_image = FileField('Изображение обложки', validators=[Optional()])
    # authors = FieldList(FormField(AuthorForm), min_entries=1, max_entries=20)
    submit = SubmitField('Сохранить изменения')



