import sqlite3
from datetime import datetime

# import click
from flask import current_app, g


def get_db():
    """
    Conecta ao banco de dados do aplicativo Flask, se ainda não estiver conectado.

    Retorna:
        sqlite3.Connection: Conexão com o banco de dados.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
    Fecha a conexão com o banco de dados, se estiver aberta.

    Args:
        e (Exception, opcional): Exceção que pode ter ocorrido.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """
    Inicializa o banco de dados executando o script SQL contido em 'schema.sql'.
    """
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


# @click.command("init-db")
# def init_db_command():
#     """Limpa os dados existentes e cria novas tabelas."""
#     init_db()
#     click.echo("Banco de dados inicializado.")


sqlite3.register_converter("timestamp", lambda v: datetime.fromisoformat(v.decode()))


def init_app(app):
    """
    Registra as funções de inicialização e encerramento do banco de dados no aplicativo Flask.

    Args:
        app (Flask): A instância do aplicativo Flask.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
