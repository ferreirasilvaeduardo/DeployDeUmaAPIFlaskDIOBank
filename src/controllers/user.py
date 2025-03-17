from http import HTTPStatus  # Importa os códigos de status HTTP

from flask import Blueprint, request  # Importa o Blueprint e request do Flask

# from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy import inspect  # Importa inspect e select do SQLAlchemy

from src.models import User, bcrypt, db
from src.utils.utils import requires_role
from src.views.user import CreateUserSchema, UserSchema

# Cria um Blueprint para o módulo de usuários
app = Blueprint("user", __name__, url_prefix="/users")


def _create_user():
    # data = request.json  # Obtém os dados da requisição
    user_schema = CreateUserSchema()
    try:
        data = user_schema.load(request.json)
    except ValidationError as err:
        return (
            err.messages,
            HTTPStatus.UNPROCESSABLE_ENTITY,
        )  # Retorna os erros de validação e o status HTTP 422, 'Unprocessable Entity'
    user = User(
        username=data["username"],
        password=bcrypt.generate_password_hash(data["password"]),
        role_id=data["role_id"],
    )  # Cria uma nova instância de User
    db.session.add(user)  # Adiciona o usuário à sessão do banco de dados
    db.session.commit()  # Confirma a transação
    return {
        "message": "Usuário criado!"
    }, HTTPStatus.CREATED  # Retorna uma mensagem de sucesso e o status HTTP 201


def _list_users(user_id=None):
    if user_id is None:
        query = db.select(User)  # Cria uma consulta para selecionar todos os usuários
        results = db.session.execute(
            query
        ).scalars()  # Executa a consulta e obtém os resultados
        user_schema = UserSchema(many=True)  # Cria uma instância de UserSchema
        return user_schema.dump(results)
        # return [
        #     {
        #         "id": result.id,
        #         "username": result.username,
        #         "role": {
        #             "id": result.role.id,
        #             "name": result.role.name,
        #         },
        #     }
        #     for result in results
        # ]  # Retorna uma lista de dicionários com os dados dos usuários
    else:
        result = db.get_or_404(
            User, user_id
        )  # Obtém o usuário pelo ID ou retorna 404 se não encontrado
        user_schema = UserSchema(many=False)  # Cria uma instância de UserSchema
        return user_schema.dump(result)
        # return [
        #     {
        #         "id": result.id,
        #         "username": result.username,
        #         "role": {
        #             "id": result.role.id,
        #             "name": result.role.name,
        #         },
        #     }
        # ]  # Retorna uma lista com um único dicionário contendo os dados do usuário


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/", methods=["GET"])
@jwt_required()
@requires_role()
def list_users():
    return {
        "users": _list_users(),
    }


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/", methods=["POST"])
def create_user():
    return _create_user()  # Chama a função para criar um novo usuário


@app.route("/<int:user_id>")
def get_user(user_id):
    """User detail view.
    ---
    get:
      parameters:
        - name: user_id
          in: path
          schema: UserIdParameter
      responses:
        200:
          description: Successful operation
          content:
            application/json:
              schema:
                UserSchema
    """

    return {"users": _list_users(user_id)}  # Retorna os dados do usuário específico


@app.route("/<int:user_id>", methods=["PATCH", "PUT"])
@jwt_required()
@requires_role()
def update_user(user_id):
    result = db.get_or_404(
        User, user_id
    )  # Obtém o usuário pelo ID ou retorna 404 se não encontrado
    data = request.json  # Obtém os dados da requisição
    executed = False  # Flag para verificar se alguma atualização foi executada
    if request.method == "PATCH" and result and data:
        if "username" in data:
            result.username = data["username"]
            db.session.commit()
            executed = (
                True  # Atualiza a flag para indicar que uma atualização foi executada
            )
    if request.method == "PUT" and result and data:
        # PUT, aconselhavel, se fosse alterar todos os campos
        attrs = inspect(User)  # Inspeciona os atributos do modelo User
        for attr in attrs.attrs:
            if attr.key in data:
                setattr(result, attr.key, data[attr.key])
                executed = True  # Atualiza a flag para indicar que uma atualização foi executada
        if "password" in data:
            pw_hash = bcrypt.generate_password_hash(data["password"])
            result.password = pw_hash
        db.session.commit()
    if result and data:
        if executed:
            # success OK = 200, 'OK', 'Request fulfilled, document follows'
            return [
                {"id": result.id, "username": result.username}
            ], HTTPStatus.OK  # Retorna os dados do usuário atualizado e o status HTTP 200
        else:
            # NOT_MODIFIED = (304, 'Not Modified','Document has not changed since given time')
            return (
                "",
                HTTPStatus.NOT_MODIFIED,
            )  # Retorna o status HTTP 304 se nenhuma atualização foi feita
    else:
        # NOT_FOUND = (404, 'Not Found', 'Nothing matches the given URI')
        return (
            "",
            HTTPStatus.NOT_FOUND,
        )  # Retorna o status HTTP 404 se o usuário não for encontrado


@app.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
@requires_role()
def delete_user(user_id):
    result = db.get_or_404(
        User, user_id
    )  # Obtém o usuário pelo ID ou retorna 404 se não encontrado
    if result:
        db.session.delete(result)  # Deleta o usuário da sessão do banco de dados
        db.session.commit()  # Confirma a transação
    if result:
        # success OK = 200, 'OK', 'Request fulfilled, document follows'
        return [
            {"id": result.id, "username": result.username}
        ], HTTPStatus.OK  # Retorna os dados do usuário deletado e o status HTTP 200
    else:
        # NOT_FOUND = (404, 'Not Found', 'Nothing matches the given URI')
        return (
            "",
            HTTPStatus.NOT_FOUND,
        )  # Retorna o status HTTP 404 se o usuário não for encontrado
