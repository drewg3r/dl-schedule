import math

from werkzeug.routing import ValidationError

from exceptions import InvalidTokenException, InvalidTokenFormatException
from service.api_token import get_user


def int_value(_min, _max=math.inf):
    """
    Validation function to use in RequestParser. Validates int values.
    Raise ValidationError if value is not valid.
    :param _min: minimum value allowed
    :param _max: maximum value allowed. Can be omitted(math.inf will be used)
    :return: value if value is valid
    """
    def validate(i):
        try:
            i = int(i)
        except ValueError:
            raise ValidationError('An integer value is required')

        if _min <= i <= _max:
            return i
        raise ValidationError(f'An integer between {_min} and {_max} is required')
    return validate


def str_length(_min, _max):
    """
    Validation function to use in RequestParser. Validates str values.
    Raise ValidationError if value is not valid.
    :param _min: minimum str length allowed
    :param _max: maximum str length allowed
    :return: value if value is valid
    """
    def validate(s):
        if isinstance(s, str):
            if _min <= len(s) <= _max:
                return s
            else:
                raise ValidationError(f'A string with length between {_min} and {_max} is required')
        else:
            raise ValidationError('A string is required')
    return validate


def api_token():
    """
    Validation function to use in RequestParser. Validates str values.
    Raise ValidationError if token does not exists.
    :return: api token if it is valid
    """
    def validate(token):
        try:
            get_user(token)
        except (InvalidTokenException, InvalidTokenFormatException, ValueError):
            raise ValidationError('Invalid API token')
        return token

    return validate
