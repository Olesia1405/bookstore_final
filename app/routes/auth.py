from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User
from ..extensions import db
from ..forms import LoginForm, RegistrationForm



bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.psw_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('main.index'))

        flash('Неверный email или пароль', 'danger')

    return render_template('auth/login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        user = User(
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data,
            psw_hash=generate_password_hash(form.password.data),
        )

        db.session.add(user)
        db.session.commit()

        flash('Код подтверждения отправлен на email', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    if request.args.get('confirm') == 'true':
        logout_user()
        flash('Вы успешно вышли из системы', 'success')
        return redirect(url_for('main.index'))
    return redirect(url_for('auth.confirm_logout'))

@bp.route('/confirm-logout')
@login_required
def confirm_logout():
    return render_template('auth/confirm_logout.html')