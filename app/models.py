from app import db, login_manager
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) #первичный ключ
    username = db.Column(db.String(64),unique=True, nullable=False)  #уникальное имя. nullable - поле не может быть пустым
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False) #шифрование пароля

    def __repr__(self):
        return f'<User:{self.username}, email:{self.email}>'#выводит имя пользователя и почту
@login_manager.user_loader #функция для загрузки пользователя из базы данных
def load_user(user_id):
    return User.query.get(int(user_id)) #загружает пользователя из базы данных

#Построение структуры таблицы базы данных


