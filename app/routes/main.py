from flask import Blueprint, render_template, request
from ..models import Book, Genre

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    limit = request.args.get("limit", default=3, type=int)
    top_books = Book.query.order_by(Book.rating.desc()).limit(limit).all()
    genres = Genre.query.all()
    return render_template('index.html', top_books=top_books, genres=genres)
