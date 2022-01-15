class AppBaseException(Exception):
    ...


class AuthException(AppBaseException):
    ...


class InvalidPasswordException(AuthException):
    ...


class UserNotFoundException(AuthException):
    ...


class InvalidTokenException(AppBaseException):
    ...


class InvalidTokenFormatException(AppBaseException):
    ...


class DuplicateSubjectNameException(AppBaseException):
    ...


class SubjectNotFoundException(AppBaseException):
    ...


class AccessDeniedException(AppBaseException):
    ...


class EventNotFoundException(AppBaseException):
    ...
