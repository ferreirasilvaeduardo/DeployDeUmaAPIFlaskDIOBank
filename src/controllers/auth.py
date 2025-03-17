from http import HTTPStatus  # Importa os códigos de status HTTP

from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from sqlalchemy import select  # Importa a função select do SQLAlchemy

from src.models import User, bcrypt, count_admin_users, db, environment

# Cria um Blueprint para o módulo de usuários
app = Blueprint("auth", __name__, url_prefix="/auth")


def _check_password(username: str, password: str):
    retorno = False
    identity = 0
    query = select(User).where(User.username == username)  # Cria a consulta
    user = db.session.execute(
        query
    ).scalar_one_or_none()  # Executa a consulta e obtém o resultado
    if user:
        identity = user.id
        # breakpoint()
        retorno = bcrypt.check_password_hash(pw_hash=user.password, password=password)
        if (
            not retorno
            and environment
            and (environment == "testing" or environment == "development")
        ):
            retorno = user.password == password
    elif (
        environment
        and (environment == "testing" or environment == "development")
        and count_admin_users() == 0
        and username == "admin"
        and password == "admin1234567890"
    ):
        retorno = True
    if retorno:
        return identity
    return None


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    identity = _check_password(username=username, password=password)
    if identity is None:
        return (
            {"msg": "Nome ou senha de usuário inválido!"},
            HTTPStatus.UNAUTHORIZED,
        )  # 401
    access_token = create_access_token(identity=str(identity))
    return {"access_token": access_token}
