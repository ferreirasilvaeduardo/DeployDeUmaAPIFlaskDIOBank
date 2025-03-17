import os

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, select  # Importa a função select e func do SQLAlchemy

from src.models.base import Base
from src.models.post import Post
from src.models.role import Role
from src.models.user import User

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
ma = Marshmallow()
environment = (
    str(os.getenv("ENVIRONMENT")).strip().lower() if os.getenv("ENVIRONMENT") else ""
)
spec = APISpec(
    title="DIO Bank",
    version="1.0.0",
    openapi_version="3.0.3",
    info=dict(description="DIO Bank API"),
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)


def count_admin_users() -> int:
    """
    Conta o número de usuários com a role 'admin'.
    """
    query = select(func.count(User.id)).join(Role).where(Role.name == "admin")
    count = db.session.execute(query).scalar()
    return count


__all__ = [
    "db",
    "migrate",
    "jwt",
    "User",
    "Role",
    "Post",
    "bcrypt",
    "environment",
    "count_admin_users",
    "ma",
]
