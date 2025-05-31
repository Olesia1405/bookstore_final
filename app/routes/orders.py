from flask import Blueprint, render_template, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from ..models import Order, CartItem, OrderItem, db
from ..forms import OrderForm

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')


@orders_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    form = OrderForm()
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()

    if not cart_items:
        flash("Ваша корзина пуста", "warning")
        return redirect(url_for("cart.view_cart"))

    # Обработка формы
    if form.validate_on_submit():
        # Проверка адреса для доставки
        if form.delivery_method.data == 'door' and not form.address.data.strip():
            flash("Укажите адрес для доставки", "danger")
            return render_template("orders/checkout.html", form=form, cart_items=cart_items)

        try:
            order = Order(
                user_id=current_user.id,
                delivery_type=form.delivery_method.data,
                address=form.address.data if form.delivery_method.data == 'door' else None,
                status="processing"
            )
            db.session.add(order)
            db.session.flush()

            # Добавляем товары в заказ
            for item in cart_items:
                order_item = OrderItem(
                    order_id=order.id,
                    book_id=item.book_id,
                    quantity=item.quantity,
                    price_at_order=item.book.price
                )
                db.session.add(order_item)
                db.session.delete(item)  # Удаляем из корзины

            db.session.commit()
            flash("Заказ успешно оформлен!", "success")
            return redirect(url_for("orders.order_details", order_id=order.id))

        except Exception as e:
            db.session.rollback()
            flash("Ошибка при оформлении заказа", "danger")
            current_app.logger.error(f"Order error: {str(e)}")

    return render_template("orders/checkout.html",
                           form=form,
                           cart_items=cart_items,
                           total_price=sum(item.book.price * item.quantity for item in cart_items))

@orders_bp.route("/history")
@login_required
def order_history():
    orders = Order.query.filter_by(user_id=current_user.id) \
        .order_by(Order.created_at.desc()) \
        .all()
    return render_template("orders/history.html", orders=orders)


@orders_bp.route("/<int:order_id>")
@login_required
def order_details(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash("Доступ запрещен", "danger")
        return redirect(url_for("main.index"))

    return render_template("orders/details.html", order=order)