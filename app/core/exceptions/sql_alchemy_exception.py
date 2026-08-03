from .app_exeception import AppException


class SqlAlchemyException(AppException):
    pass


class IntegrityViolationException(SqlAlchemyException):
    def __init__(self, message="Integrity constraint violation", details: dict = {}):
        super().__init__(message, 409, details)


class DatabaseUnavailableException(SqlAlchemyException):
    def __init__(self, message="Database unavailable", details: dict = {}):
        super().__init__(message, 503, details)
