from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, StringField, SubmitField, TextAreaField, FieldList, FormField, BooleanField
from wtforms.validators import DataRequired, Length, URL, Optional
from flask_wtf.file import FileAllowed, FileField, FileRequired


class Select2MultipleField(SelectMultipleField):
    def pre_validate(self, form):
        # Отключение ошибки "not a valid choice"
        pass


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
    publication_date = StringField('Дата публикации', validators=[Length(max=50)])
    publisher = StringField('Издатель', validators=[Length(max=200)])
    telegram_link = StringField('Telegram Link', validators=[Length(max=200)])
    telegram_file_id = StringField('Telegram File ID', validators=[Length(max=200)])
    description = TextAreaField('Описание')
    authors = Select2MultipleField('Авторы', choices=[], validators=[])
    categories = Select2MultipleField('Категории', choices=[], validators=[])
    submit = SubmitField('Сохранить')
