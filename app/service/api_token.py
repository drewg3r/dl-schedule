import uuid

from exceptions import InvalidTokenException, InvalidTokenFormatException
from models import User, ApiToken


def get_user(token: str | int) -> User:
    """
    Get user by his token.
    Raise InvalidTokenFormatException if token is not valid UUID.
    Raise InvalidTokenException if token is not in database.
    :param token: hex or int token
    :return: instance of User model class
    """
    try:
        token = ApiToken.query.filter_by(token=uuid.UUID(str(token)).hex).first()
    except ValueError:
        raise InvalidTokenFormatException
    if token:
        return token.user
    else:
        raise InvalidTokenException


def get_primary_token(user: User) -> ApiToken:
    """
    Get user's primary API token.
    """
    return ApiToken.query.filter(ApiToken.is_primary == True, ApiToken.user == user).first()
