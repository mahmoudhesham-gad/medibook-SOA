from flask import jsonify
from pydantic import ValidationError as PydanticValidationError
from werkzeug.exceptions import HTTPException


class AppError(Exception):
    status = 500
    code = "INTERNAL_ERROR"

    def __init__(self, message, code=None):
        super().__init__(message)
        self.message = message
        if code:
            self.code = code


class ValidationError(AppError):
    status, code = 400, "VALIDATION_ERROR"


class InvalidCredentialsError(AppError):
    status, code = 401, "INVALID_CREDENTIALS"


class NotFoundError(AppError):
    status, code = 404, "NOT_FOUND"


class ConflictError(AppError):
    status, code = 409, "CONFLICT"


class ServiceUnavailableError(AppError):
    status, code = 503, "SERVICE_UNAVAILABLE"


def _body(code, message):
    return {"error": {"code": code, "message": message}}


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(e):
        return jsonify(_body(e.code, e.message)), e.status

    @app.errorhandler(PydanticValidationError)
    def handle_pydantic_error(e):
        message = "; ".join(
            f"{'.'.join(str(p) for p in err['loc'])}: {err['msg']}"
            for err in e.errors()
        )
        return jsonify(_body("VALIDATION_ERROR", message)), 400

    @app.errorhandler(HTTPException)
    def handle_http_error(e):
        codes = {400: "VALIDATION_ERROR", 404: "NOT_FOUND", 405: "METHOD_NOT_ALLOWED"}
        return jsonify(_body(codes.get(e.code, "HTTP_ERROR"), e.description)), e.code

    @app.errorhandler(Exception)
    def handle_unexpected(e):
        app.logger.exception(e)
        return jsonify(_body("INTERNAL_ERROR", "Unexpected server error")), 500
