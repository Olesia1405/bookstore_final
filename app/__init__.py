from flask import Flask
from app.extensions import db, login_manager
from app.models import Book, BookGenre, CartItem, OrderItem, Order, Review, User
from app.utils import initialize_books
from config import settings
from app.routes.auth import bp as auth_bp
from app.routes.main import bp as main_bp
from app.routes.cart import cart_bp
from app.routes.orders import orders_bp



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = settings.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI


    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)

    with app.app_context():
        db.create_all()
        initialize_books()

    return app
