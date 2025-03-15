from functools import wraps
from http import HTTPStatus  # Importa os códigos de status HTTP

from flask_jwt_extended import get_jwt_identity

from src.app import User, db  # Importa o modelo User e a instância do banco de dados


def requires_role(role_id=None, role_name=None):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Access the identity of the current user with get_jwt_identity
            current_user_id = get_jwt_identity()
            result = db.get_or_404(User, current_user_id)
            if not result:
                return {"msg": "Usuário inválido"}, HTTPStatus.UNAUTHORIZED  # 401
            if (role_id and result.role.id != role_id) or (
                role_name
                and str(result.role.name).strip().upper()
                != str(role_name).strip().upper()
            ):
                return {
                    "msg": "Usuário não tem permissão!"
                }, HTTPStatus.FORBIDDEN  # 403
            return f(*args, **kwargs)

        return wrapped

    return decorator


def requires_role_name(role_name):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Access the identity of the current user with get_jwt_identity
            current_user_id = get_jwt_identity()
            result = db.get_or_404(User, current_user_id)
            if not result:
                return {"msg": "Usuário inválido"}, HTTPStatus.UNAUTHORIZED  # 401
            if (
                role_name
                and str(result.role.name).strip().upper()
                != str(role_name).strip().upper()
            ):
                return {
                    "msg": "Usuário não tem permissão!"
                }, HTTPStatus.FORBIDDEN  # 403
            return f(*args, **kwargs)

        return wrapped

    return decorator


def eleva_quadrado(numero):
    return numero**2
