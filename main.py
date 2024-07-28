from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False) #unique означает, что поле должно быть уникальным, nullable означает, что поле не может быть пустым

    def __repr__(self): #repr определяет строковое представление объекта
        return '<User %r>' % self.username


def init_db(): #функция для инициализации базы данных
    db.create_all()
@app.route('/add_user')
def add_user():
    user = User(username='john')
    db.session.add(user)
    db.session.commit()
    return 'User added!'

@app.route('/users')
def users():
    users = User.query.all()
    return str(users)

if __name__ == '__main__':
    init_db()
    app.run()