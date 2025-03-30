from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class AuthorForm(FlaskForm):
    name = StringField(
        "Имя",
        validators=[
            DataRequired(message="Имя обязательно для заполнения."),
            Length(max=100, message="Имя не должно превышать 100 символов."),
        ],
    )
    name_eng = StringField(
        "Имя на английском",
    )
    submit = SubmitField("Сохранить")
