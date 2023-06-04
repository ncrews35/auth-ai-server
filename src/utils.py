import json
from enum import Enum

__all__ = [
    "ErrorCode",
    "error"
]


class ErrorCode(Enum):
    INVALID_REQUEST = "invalid_request"
    INVALID_CLIENT = "invalid_client"
    INVALID_GRANT = "invalid_grant"
    UNAUTHORIZED_CLIENT = "unauthorized_client"
    UNSUPPORTED_GRANT_TYPE = "unsupported_grant_type"
    INVALID_SCOPE = "invalid_scope"
    SERVER_ERROR = "server_error"
    TEMPORARILY_UNAVAILABLE = "temporarily_unavailable"


def error(error_code: ErrorCode, error_description: str):
    return {
        "code": error_code.value,
        "description": error_description
    }, status_code(error_code)


def status_code(error_code: ErrorCode):
    if error_code == ErrorCode.INVALID_REQUEST:
        return 400
    elif error_code == ErrorCode.INVALID_CLIENT:
        return 401
    elif error_code == ErrorCode.INVALID_GRANT:
        return 401
    elif error_code == ErrorCode.UNAUTHORIZED_CLIENT:
        return 401
    elif error_code == ErrorCode.UNSUPPORTED_GRANT_TYPE:
        return 400
    elif error_code == ErrorCode.INVALID_SCOPE:
        return 400
    elif error_code == ErrorCode.SERVER_ERROR:
        return 500
    elif error_code == ErrorCode.TEMPORARILY_UNAVAILABLE:
        return 503
    else:
        return 500
