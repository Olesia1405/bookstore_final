from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from app.models import User  # импорт внутри функции — избегаем цикла
    return User.query.get(int(user_id))
