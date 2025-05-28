from app.models import Book, Genre, BookGenre
from app.extensions import db
from pathlib import Path
import json
from datetime import datetime, timezone

def initialize_books():
    if Book.query.first() is not None:
        return

    json_path = Path(__file__).parent / 'books_catalog.json'

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            books_data = json.load(f)

        for book_data in books_data:
            cover_path = book_data.get('cover')

            genre_name = book_data.get('genre')
            genre = None
            if genre_name:
                genre = Genre.query.filter_by(name=genre_name).first()
                if not genre:
                    genre = Genre(name=genre_name)
                    db.session.add(genre)
                    db.session.commit()

            book = Book(
                title=book_data['title'],
                author=book_data['author'],
                price=float(book_data['price']),
                cover=cover_path,
                description=book_data.get('description'),
                rating=float(book_data.get('rating', 0.0))
            )
            db.session.add(book)
            db.session.flush()  # чтобы получить book.id

            if genre:
                # Создаём объект ассоциации BookGenre вручную с created_at
                association = BookGenre(
                    book_id=book.id,
                    genre_id=genre.id,
                    created_at=datetime.now(timezone.utc)
                )
                db.session.add(association)

        db.session.commit()
        print("✅ Книги успешно загружены в БД")

    except Exception as e:
        print(f"❌ Ошибка: {str(e)}")
        db.session.rollback()
