from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import login_required, current_user
from ..models import CartItem, Book, db

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')


@cart_bp.route('/')
@login_required
def view_cart():
    items = CartItem.query.filter_by(user_id=current_user.id).join(Book).all()
    total_price = sum(item.book.price * item.quantity for item in items)
    return render_template('cart/cart.html', items=items, total_price=total_price)


@cart_bp.route('/add/<int:book_id>', methods=['POST'])
@login_required
def add_to_cart(book_id):
    book = Book.query.get_or_404(book_id)

    item = CartItem.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    if item:
        item.quantity += 1
    else:
        item = CartItem(user_id=current_user.id, book_id=book_id, quantity=1)
        db.session.add(item)

    db.session.commit()
    flash(f'"{book.title}" добавлена в корзину', 'success')
    return redirect(request.referrer or url_for('books.catalog'))


@cart_bp.route('/update/<int:item_id>', methods=['POST'])
@login_required
def update_quantity(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        flash("Нет доступа", 'danger')
        return redirect(url_for('cart.view_cart'))

    try:
        new_quantity = int(request.form['quantity'])
        if new_quantity < 1:
            raise ValueError
        item.quantity = new_quantity
        db.session.commit()
        flash('Количество обновлено', 'success')
    except (ValueError, KeyError):
        flash('Некорректное количество', 'danger')

    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        flash("Нет доступа", 'danger')
        return redirect(url_for('cart.view_cart'))

    db.session.delete(item)
    db.session.commit()
    flash('Товар удален из корзины', 'success')
    return redirect(url_for('cart.view_cart'))

