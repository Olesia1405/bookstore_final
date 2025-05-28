from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from ..models import CartItem, Book, OrderItem, Order
from ..extensions import db

cart_bp = Blueprint('cart', __name__, url_prefix='cart')

@cart_bp.route('/')
@login_required
def view_cart():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    return render_template('cart/cart.html', items=items)

@cart_bp.route('/add/<int:book_id>', methods=['POST'])
@login_required
def add_to_cart(book_id):
    item = CartItem.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    if item:
        item.quantity += 1
    else:
        item = CartItem(user_id=current_user.id, book_id=book_id, quantity=1)
        db.session.add(item)
    db.session.commit()
    flash('Книга добавлена в корзину', 'success')
    return redirect(url_for('books.book', book_id=book_id))

@cart_bp.route('/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        flash("Вы не можете удалить этот товар", 'danger')
        return redirect(url_for('cart.cart'))

    db.session.delete(item)
    db.session.commit()
    flash('Товар удален из корзины', 'success')
    return redirect(url_for('cart.cart'))


