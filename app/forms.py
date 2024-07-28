from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm): #создаем форму регистрации
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Регистрация')
    # confirm password  подтверждение пароля equal to повторное введение пароля
    #submit - кнопка отправки формы
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first() #обращаемся к базе данных , с помощью фильтра, ищем пользователя с таким именем
        if user:
            raise ValidationError('Такой пользователь уже существует. Пожалуйста, выберите другое имя.') #raise - исключение ошибки

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Такой почтовый адрес уже существует. Пожалуйста, выберите другой.')
class LoginForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня') #Можно войти без пароля (BooleanField галочка позволяет это сделать)
    submit = SubmitField('Войти')
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Старый пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите  новый пароль', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Сменить пароль')
class ChangeEmailForm(FlaskForm):
    email = StringField('Новая почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Сменить почту')
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Такой почтовый адрес уже существует. Пожалуйста, выберите другой.')
class ChangeUsernameForm(FlaskForm):
    username = StringField('Новое имя пользователя', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Сменить имя пользователя')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first() #обращаемся к базе данных , с помощью фильтра, ищем пользователя с таким именем
        if user:
            raise ValidationError('Такой пользователь уже существует. Пожалуйста, выберите другое имя.')

