from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import logout_user

from exceptions import InvalidPasswordException, UserNotFoundException
from service.auth import sign_in, sign_up

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('auth/sign-in.html')

    username = request.form.get('username', None)
    password = request.form.get('password', None)

    if username and password:
        try:
            sign_in(username, password)
        except InvalidPasswordException:
            flash('Invalid password')
        except UserNotFoundException:
            flash('Invalid username')
        else:
            return redirect(url_for('schedule.index_page'))

    return redirect(url_for("auth.login_page"))


@bp.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'GET':
        return render_template('auth/sign-up.html')

    username = request.form.get('username', None)
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    password2 = request.form.get('password2', None)

    if username and password and password2:
        if password == password2:
            sign_up(username=username, email=email, password=password)
            flash(f'{username}, your account has been created', 'success')
            return redirect(url_for('schedule.index_page'))
        else:
            flash('Passwords don\'t match', 'danger')
    else:
        flash('Please provide your username and password', 'warning')

    return redirect(url_for('auth.signup_page'))


@bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('index.index_page'))
