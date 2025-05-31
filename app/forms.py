from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional, Regexp
from .models import User

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=36)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField("Телефон", validators=[
        DataRequired(),
        Regexp(r'^\+?[78]\d{10}$', message="Введите корректный номер телефона")
    ])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=36)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Этот email уже занят')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя пользователя уже занято')


class OrderForm(FlaskForm):
    delivery_method = SelectField(
        'Способ доставки',
        choices=[
            ('pickup', 'Самовывоз'),
            ('door', 'Доставка курьером')
        ],
        validators=[DataRequired()],
        id="delivery_method"  # Добавляем ID для JavaScript
    )

    address = TextAreaField(
        'Адрес доставки',
        validators=[
            Optional(),
            Length(min=10, message="Адрес должен содержать минимум 10 символов")
        ],
        render_kw={
            "placeholder": "Улица, дом, квартира",
            "rows": 3,
            "id": "address_field"
        }
    )

    submit = SubmitField('Подтвердить заказ')