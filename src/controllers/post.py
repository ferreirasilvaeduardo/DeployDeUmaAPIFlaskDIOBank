from http import HTTPStatus  # Importa os códigos de status HTTP

from flask import Blueprint, request  # Importa o Blueprint e request do Flask
from sqlalchemy import inspect  # Importa inspect do SQLAlchemy

from src.models import Post, db

# Cria um Blueprint para o módulo de posts
app = Blueprint("post", __name__, url_prefix="/posts")


def _create_post():
    data = request.json  # Obtém os dados da requisição
    post = Post(
        title=data["title"],
        body=data.get("body", "N/A"),
        author_id=data["author_id"],
    )  # Cria uma nova instância de Post
    db.session.add(post)  # Adiciona o post à sessão do banco de dados
    db.session.commit()  # Confirma a transação


def _list_posts(post_id=None):
    if post_id is None:
        query = db.select(Post)  # Cria uma consulta para selecionar todos os posts
        results = db.session.execute(
            query
        ).scalars()  # Executa a consulta e obtém os resultados
        return [
            {
                "id": result.id,
                "title": result.title,
                "body": result.body,
                "author_id": result.author_id,
            }
            for result in results
        ]  # Retorna uma lista de dicionários com os dados dos posts
    else:
        result = db.get_or_404(
            Post, post_id
        )  # Obtém o post pelo ID ou retorna 404 se não encontrado
        return [
            {
                "id": result.id,
                "title": result.title,
                "body": result.body,
                "author_id": result.author_id,
            }
        ]  # Retorna uma lista com um único dicionário contendo os dados do post


@app.route("/", methods=["GET", "POST"])
def handle_post():
    if request.method == "POST":
        _create_post()  # Chama a função para criar um novo post
        return {
            "message": "Postagem criada!"
        }, HTTPStatus.CREATED  # Retorna uma mensagem de sucesso e o status HTTP 201
    elif request.method == "GET":
        return {"posts": _list_posts()}  # Retorna a lista de posts
    else:
        raise ValueError(
            "Método inválido!" + str(request.method)
        )  # Lança um erro para métodos inválidos


@app.route("/<int:post_id>")
def get_post(post_id):
    return {"posts": _list_posts(post_id)}  # Retorna os dados do post específico


@app.route("/<int:post_id>", methods=["PATCH", "PUT"])
def update_post(post_id):
    result = db.get_or_404(
        Post, post_id
    )  # Obtém o post pelo ID ou retorna 404 se não encontrado
    data = request.json  # Obtém os dados da requisição
    executed = False  # Flag para verificar se alguma atualização foi executada
    if request.method == "PATCH" and result and data:
        if "title" in data:
            result.title = data["title"]
            db.session.commit()
            executed = (
                True  # Atualiza a flag para indicar que uma atualização foi executada
            )
    if request.method == "PUT" and result and data:
        # PUT, aconselhavel, se fosse alterar todos os campos
        attrs = inspect(Post)  # Inspeciona os atributos do modelo Post
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
                    "title": result.title,
                    "body": result.body,
                    "author_id": result.author_id,
                }
            ], HTTPStatus.OK  # Retorna os dados do post atualizado e o status HTTP 200
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
        )  # Retorna o status HTTP 404 se o post não for encontrado


@app.route("/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    result = db.get_or_404(
        Post, post_id
    )  # Obtém o post pelo ID ou retorna 404 se não encontrado
    if result:
        db.session.delete(result)  # Deleta o post da sessão do banco de dados
        db.session.commit()  # Confirma a transação
    if result:
        # success OK = 200, 'OK', 'Request fulfilled, document follows'
        return [
            {
                "id": result.id,
                "title": result.title,
                "body": result.body,
                "author_id": result.author_id,
            }
        ], HTTPStatus.OK  # Retorna os dados do post deletado e o status HTTP 200
    else:
        # NOT_FOUND = (404, 'Not Found', 'Nothing matches the given URI')
        return (
            "",
            HTTPStatus.NOT_FOUND,
        )  # Retorna o status HTTP 404 se o post não for encontrado
