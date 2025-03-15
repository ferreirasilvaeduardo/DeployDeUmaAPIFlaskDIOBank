from http import HTTPStatus  # Importa os códigos de status HTTP

from flask import Blueprint, request  # Importa o Blueprint e request do Flask
from sqlalchemy import inspect  # Importa inspect do SQLAlchemy

from src.app import Role, db  # Importa o modelo Role e a instância do banco de dados

# Cria um Blueprint para o módulo de roles
app = Blueprint("role", __name__, url_prefix="/roles")


def _create_role():
    """
    Cria um novo role com os dados fornecidos na requisição.
    """
    data = request.json  # Obtém os dados da requisição
    role = Role(
        name=data["name"],
    )  # Cria uma nova instância de Role
    db.session.add(role)  # Adiciona o role à sessão do banco de dados
    db.session.commit()  # Confirma a transação


def _list_roles(role_id=None):
    """
    Lista todos os roles ou um role específico se o role_id for fornecido.

    :param role_id: ID do role a ser listado (opcional)
    :return: Lista de roles ou um role específico
    """
    if role_id is None:
        query = db.select(Role)  # Cria uma consulta para selecionar todos os roles
        results = db.session.execute(
            query
        ).scalars()  # Executa a consulta e obtém os resultados
        return [
            {
                "id": result.id,
                "name": result.name,
            }
            for result in results
        ]  # Retorna uma lista de dicionários com os dados dos roles
    else:
        result = db.get_or_404(
            Role, role_id
        )  # Obtém o role pelo ID ou retorna 404 se não encontrado
        return [
            {
                "id": result.id,
                "name": result.name,
            }
        ]  # Retorna uma lista com um único dicionário contendo os dados do role


@app.route("/", methods=["GET", "POST"])
def handle_role():
    """
    Manipula requisições GET e POST para criar ou listar roles.

    :return: Mensagem de sucesso ou lista de roles
    """
    if request.method == "POST":
        _create_role()  # Chama a função para criar um novo role
        return {
            "message": "Role criada!"
        }, HTTPStatus.CREATED  # Retorna uma mensagem de sucesso e o status HTTP 201
    elif request.method == "GET":
        return {"roles": _list_roles()}  # Retorna a lista de roles
    else:
        raise ValueError(
            "Método inválido!" + str(request.method)
        )  # Lança um erro para métodos inválidos


@app.route("/<int:role_id>")
def get_role(role_id):
    """
    Obtém um role específico pelo ID.

    :param role_id: ID do role a ser obtido
    :return: Dados do role
    """
    return {"roles": _list_roles(role_id)}  # Retorna os dados do role específico


@app.route("/<int:role_id>", methods=["PATCH", "PUT"])
def update_role(role_id):
    """
    Atualiza um role específico pelo ID usando métodos PATCH ou PUT.

    :param role_id: ID do role a ser atualizado
    :return: Dados do role atualizado ou status de erro
    """
    result = db.get_or_404(
        Role, role_id
    )  # Obtém o role pelo ID ou retorna 404 se não encontrado
    data = request.json  # Obtém os dados da requisição
    executed = False  # Flag para verificar se alguma atualização foi executada
    if request.method == "PATCH" and result and data:
        if "name" in data:
            result.name = data["name"]
            db.session.commit()
            executed = (
                True  # Atualiza a flag para indicar que uma atualização foi executada
            )
    if request.method == "PUT" and result and data:
        # PUT, aconselhavel, se fosse alterar todos os campos
        attrs = inspect(Role)  # Inspeciona os atributos do modelo Role
        for attr in attrs.attrs:
            if attr.key in data:
                setattr(result, attr.key, data[attr.key])
                executed = True  # Atualiza a flag para indicar que uma atualização foi executada
        db.session.commit()
    if result and data:
        if executed:
            # success OK = 200, 'OK', 'Request fulfilled, document follows'
            return [
                {
                    "id": result.id,
                    "name": result.name,
                }
            ], HTTPStatus.OK  # Retorna os dados do role atualizado e o status HTTP 200
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
        )  # Retorna o status HTTP 404 se o role não for encontrado


@app.route("/<int:role_id>", methods=["DELETE"])
def delete_role(role_id):
    """
    Deleta um role específico pelo ID.

    :param role_id: ID do role a ser deletado
    :return: Dados do role deletado ou status de erro
    """
    result = db.get_or_404(
        Role, role_id
    )  # Obtém o role pelo ID ou retorna 404 se não encontrado
    if result:
        db.session.delete(result)  # Deleta o role da sessão do banco de dados
        db.session.commit()  # Confirma a transação
    if result:
        # success OK = 200, 'OK', 'Request fulfilled, document follows'
        return [
            {
                "id": result.id,
                "name": result.name,
            }
        ], HTTPStatus.OK  # Retorna os dados do role deletado e o status HTTP 200
    else:
        # NOT_FOUND = (404, 'Not Found', 'Nothing matches the given URI')
        return (
            "",
            HTTPStatus.NOT_FOUND,
        )  # Retorna o status HTTP 404 se o role não for encontrado
