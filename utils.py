from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError
from functools import wraps
from flask_restplus import abort

from orm import get_user_by_id, to_json


def jwt_required_silent(function):
    """A 'better' jwt_required decorator that avoids sending 500 errors on wrong auth parameters."""
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return jwt_required(function)(*args, **kwargs)
        except (NoAuthorizationError, InvalidHeaderError):
            return abort(401)
    return wrapper


def admin_required(function):
    def is_admin(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            user = to_json(get_user_by_id.first(get_jwt_identity()))
            if not user['is_admin']:
                return abort(401)
            return function(*args, **kwargs)
        return wrapper

    @wraps(function)
    def wrapper(*args, **kwargs):
        return jwt_required_silent(is_admin(function))(*args, **kwargs)
    return wrapper
