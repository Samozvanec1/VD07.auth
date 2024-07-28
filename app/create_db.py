from app import db, app
from app.models import User

with app.app_context():
    db.create_all()

# создаёт базу данных если ее нет