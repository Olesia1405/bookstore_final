from flask import Blueprint, flash, redirect, url_for, render_template
from ..models import Book, Genre
from ..extensions import db


books_bp = Blueprint('books', __name__, url_prefix='/books')

@books_bp.route('/<int:book_id>')
def get_books(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('books/book.html', book=book)

@books_bp.route('/catalog')
def get_book_catalog():
    genres = Genre.query.all()
    return render_template('books/catalog.html', genres=genres)

@books_bp.route('/genre/<int:genre_id>')
def get_book_by_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    books = genre.books
    return render_template('books/genre_books.html')



