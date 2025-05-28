from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from ..models import Order, CartItem, OrderItem
from ..extensions import db
from ..forms import OrderForm

orders_bp = Blueprint('orders', __name__, url_prefix='orders')


@orders_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    form = OrderForm()
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()

    if not cart_items:
        flash("Ваша корзина пуста.")
        return redirect(url_for("cart.view_cart"))

    if form.validate_on_submit():
        order = Order(
            user_id=current_user.id,
            delivery_method=form.delivery_method.data,
            address=form.address.data if form.delivery_method.data == "door" else None
        )
        db.session.add(order)
        db.session.flush()  # Чтобы получить order.id до коммита

        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                book_id=item.book_id,
                quantity=item.quantity,
                price=item.book.price
            )
            db.session.add(order_item)

        # Очистим корзину
        for item in cart_items:
            db.session.delete(item)

        db.session.commit()
        flash("Заказ оформлен!")
        return redirect(url_for("order.order_history"))

    return render_template("order/checkout.html", form=form, cart_items=cart_items)
