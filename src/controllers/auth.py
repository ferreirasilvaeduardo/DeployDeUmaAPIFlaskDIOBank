from http import HTTPStatus  # Importa os códigos de status HTTP

from flask import Blueprint, Flask, request
from flask_jwt_extended import create_access_token
from sqlalchemy import select  # Importa a função select do SQLAlchemy

from src.app import User, db  # Importa o modelo User e a instância do banco de dados

# Cria um Blueprint para o módulo de usuários
app = Blueprint("auth", __name__, url_prefix="/auth")


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    query = select(User).where(User.username == username)  # Cria a consulta
    user = db.session.execute(
        query
    ).scalar_one_or_none()  # Executa a consulta e obtém o resultado
    if not user or user.password != password:
        return (
            {"msg": "Nome ou senha de usuário inválido!"},
            HTTPStatus.UNAUTHORIZED,
        )  # 401

    access_token = create_access_token(identity=str(user.id))
    return {"access_token": access_token}
