from flask import flash
from flask_login import login_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

from exceptions import InvalidPasswordException, UserNotFoundException
from models import User, ApiToken
from app import db, login_manager


def sign_in(username: str, password: str) -> None:
    """
    Sign in user by username and password.
    Raise InvalidPasswordException if an incorrect password is passed.
    Raise UserNotFoundException in case username is not found in database.
    :param username: user's username
    :param password: user's password
    :return: None
    """
    user = User.query.filter_by(username=username).first()

    if user:
        if check_password_hash(user.password, password):
            login_user(user)
            return
        else:
            raise InvalidPasswordException
    else:
        raise UserNotFoundException


def sign_up(username: str, email: str, password: str) -> None:
    """
    Create new user record.
    :param username: user's username
    :param email: user's email
    :param password: user's password
    :return:
    """
    hashed_password = generate_password_hash(password)
    user = User(username=username, email=email, password=hashed_password)
    primary_api_token = ApiToken(name='Primary API key', is_primary=True, user=user)
    db.session.add(user, primary_api_token)
    db.session.commit()
    login_user(user)


@login_manager.unauthorized_handler
def unauthorized_callback():
    """
    Called in methods decorated with @login_required if current user is
    not authenticated.
    :return:
    """
    flash('Please login to access this page')
    return redirect('/login')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
