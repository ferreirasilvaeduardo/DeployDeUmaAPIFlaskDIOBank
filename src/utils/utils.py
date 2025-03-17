from functools import wraps
from http import HTTPStatus  # Importa os códigos de status HTTP

from flask_jwt_extended import get_jwt_identity

from src.models import User, count_admin_users, db, environment


def requires_role(role_id=None, role_name="admin"):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Access the identity of the current user with get_jwt_identity
            current_user_id = get_jwt_identity()
            if current_user_id is None:
                return "", HTTPStatus.NOT_FOUND  # 404
            elif str(current_user_id).strip() == "0":
                current_user_id = int(current_user_id)
                if (
                    environment
                    and (environment == "testing" or environment == "development")
                    and count_admin_users() == 0
                ):
                    return f(*args, **kwargs)
            user = db.get_or_404(User, current_user_id)
            if user:
                if (role_id and user.role.id != role_id) or (
                    role_name
                    and str(user.role.name).strip().upper()
                    != str(role_name).strip().upper()
                ):
                    return {
                        "msg": "Usuário não tem permissão!"
                    }, HTTPStatus.FORBIDDEN  # 403
                else:
                    return f(*args, **kwargs)
            else:
                return {
                    "msg": "Usuário não tem permissão!"
                }, HTTPStatus.FORBIDDEN  # 403

        return wrapped

    return decorator


def requires_role_name(role_name="admin"):
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
