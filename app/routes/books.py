from flask import Blueprint, redirect, url_for, render_template, request
from ..models import Book, Genre


books_bp = Blueprint('books', __name__, url_prefix='/books')

@books_bp.route('/<int:book_id>')
def get_books(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('books/book.html', book=book)

@books_bp.route('/catalog')
def get_book_catalog():
    genres = Genre.query.all()
    top_books = Book.query.order_by(Book.rating.desc()).limit(4).all()
    return render_template('books/catalog.html', genres=genres,
                           top_books=top_books)

@books_bp.route('/genre/<int:genre_id>')
def get_book_by_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    books = genre.books  # Получаем книги через отношение
    return render_template('books/genre_books.html', genre=genre, books=books)


@books_bp.route('/search')
def search():
    query = request.args.get('q', '').strip().capitalize()
    if not query:
        return redirect(url_for('books.get_book_catalog'))

    # Ищем по названию и автору
    books = Book.query.filter(
        Book.title.ilike(f'%{query}%') |
        Book.author.ilike(f'%{query}%')
    ).all()

    return render_template('books/search_results.html',
                           books=books,
                           query=query)



