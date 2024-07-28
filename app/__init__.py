from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you never hak this password' #ключ для шифрования пароля
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ОдноИзвилистая.db' #путь к базе данных
db = SQLAlchemy(app) #создание базы данных
bcrypt = Bcrypt(app) #шифрование пароля
login_manager = LoginManager(app) #авторизация
login_manager.login_view = 'login' #страница с которой пользователь перенаправляется при неавторизованном доступе

from app import routes

# подгрузка библиотеки для работы с базой данных. базы данных находится в папке instance
# основные данные для работы