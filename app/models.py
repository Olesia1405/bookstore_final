from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db
from datetime import datetime, timezone
from sqlalchemy.orm import validates


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    psw_hash = db.Column(db.String(256), nullable=False)

    orders = db.relationship("Order", back_populates="user", cascade="all, delete-orphan")
    cart_items = db.relationship("CartItem", back_populates="user")


class BookGenre(db.Model):
    __tablename__ = "book_genres"

    book_id = db.Column(db.Integer, db.ForeignKey("books.id", ondelete="CASCADE"), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Добавляем overlaps, чтобы устранить предупреждения
    book = db.relationship("Book", back_populates="genre_associations", overlaps="genres,books")
    genre = db.relationship("Genre", back_populates="book_associations", overlaps="books,genres")


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    cover = db.Column(db.String(255))
    description = db.Column(db.Text)
    rating = db.Column(db.Float, default=0.0)

    genre_associations = db.relationship(
        "BookGenre",
        back_populates="book",
        cascade="all, delete-orphan",
        overlaps="genres"
    )
    genres = db.relationship(
        "Genre",
        secondary="book_genres",
        back_populates="books",
        overlaps="genre_associations,book_associations"
    )


class Genre(db.Model):
    __tablename__ = "genres"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    # Отношения
    book_associations = db.relationship(
        "BookGenre",
        back_populates="genre",
        cascade="all, delete-orphan",
        overlaps="books"
    )
    books = db.relationship(
        "Book",
        secondary="book_genres",
        back_populates="genres",
        overlaps="book_associations,genre_associations"
    )



class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    user = db.relationship("User", back_populates="cart_items")
    book = db.relationship('Book', backref=db.backref('in_carts', lazy=True))


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(20), default='processing')
    address = db.Column(db.Text)
    delivery_type = db.Column(db.String(20))

    user = db.relationship('User', back_populates='orders')
    items = db.relationship('OrderItem', backref='order', lazy=True)

    @validates('address')
    def validate_address(self, key, address):
        if self.delivery_type == 'door' and not address:
            raise ValueError("Адрес обязателен для доставки")
        return address


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_order = db.Column(db.Float, nullable=False)

    book = db.relationship('Book', backref=db.backref('in_orders', lazy=True))


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    book = db.relationship('Book', backref=db.backref('reviews', lazy=True))








