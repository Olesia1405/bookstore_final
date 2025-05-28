from flask import Blueprint, render_template
from ..models import Book

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    top_books = Book.query.order_by(Book.rating.desc()).limit(3).all()
    return render_template('index.html', top_books=top_books)