class AppBaseException(Exception):
    ...


class AuthException(AppBaseException):
    ...


class InvalidPasswordException(AuthException):
    ...


class UserNotFoundException(AuthException):
    ...
