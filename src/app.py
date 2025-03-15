import os
from datetime import datetime

import click
import sqlalchemy as sa
from flask import Flask, current_app
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Classe base para modelos SQLAlchemy."""

    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
jwt = JWTManager()


class Role(db.Model):
    """Modelo representando um Role/Papel ou Grupo de permissão."""

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False)
    user: Mapped[list["User"]] = relationship(back_populates="role")

    def __repr__(self) -> str:
        """Retorna uma representação em string do Role."""
        return f"Role(id={self.id!r}, name={self.name!r})"


class User(db.Model):
    """Modelo representando um usuário."""

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sa.String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(sa.String, nullable=False)
    role_id: Mapped[int] = mapped_column(sa.ForeignKey("role.id"))
    role: Mapped["Role"] = relationship(back_populates="user")

    def __repr__(self) -> str:
        """Retorna uma representação em string do User."""
        return f"User(id={self.id!r}, username={self.username!r})"


class Post(db.Model):
    """Modelo representando uma postagem no blog."""

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(sa.String, nullable=False)
    body: Mapped[str] = mapped_column(sa.String, nullable=False)
    created: Mapped[datetime] = mapped_column(
        sa.DateTime, nullable=False, server_default=sa.func.now()
    )
    author_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"))

    def __repr__(self) -> str:
        """Retorna uma representação em string do Post."""
        return (
            f"Post(id={self.id!r}, title={self.title!r}, author_id={self.author_id!r})"
        )


@click.command("init-db")
def init_db_command():
    """Limpa os dados existentes e cria novas tabelas."""
    # Inicializa o banco de dados criando todas as tabelas
    global db
    with current_app.app_context():
        db.create_all()
    click.echo("Banco de dados inicializado.")


def create_app(test_config=None):
    """
    Cria e configura a aplicação Flask.

    Args:
        test_config (dict, optional): Dicionário de configuração para testes. Padrão é None.

    Returns:
        Flask: Aplicação Flask configurada.
    """
    app = Flask(__name__, instance_relative_config=True)

    # Define a configuração padrão
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI=os.environ["DATABASE_URL"],  # Configura o banco de dados SQLite
        # SQLALCHEMY_DATABASE_URI="sqlite:///blog.sqlite",  # Configura o banco de dados SQLite
        # SQLALCHEMY_TRACK_MODIFICATIONS=False,  # Desativa track modifications para economizar recursos
        JWT_SECRET_KEY="super-secret",  # Change this! JWTManager # Setup the Flask-JWT-Extended extension
    )

    if test_config is None:
        # Carrega a configuração da instância, se existir, quando não estiver testando
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Carrega a configuração de teste se passada
        app.config.from_mapping(test_config)

    # Garante que a pasta da instância exista
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Define uma rota simples que retorna uma mensagem de boas-vindas
    @app.route("/")
    def home():
        """Retorna uma mensagem de boas-vindas."""
        return "Olá, Seja bem vindo!"

    # Registra comandos CLI
    app.cli.add_command(init_db_command)
    # Inicializa a aplicação com a extensão SQLAlchemy
    db.init_app(app)
    # Inicializa a aplicação com a extensão Flask-Migrate
    migrate.init_app(app, db)
    # Inicializa a aplicação com a extensão Flask-JWT-Extended
    jwt.init_app(app)

    # Importa e registra blueprints para os controladores
    from src.controllers import user as user_controller

    app.register_blueprint(user_controller.app)

    from src.controllers import post as post_controller

    app.register_blueprint(post_controller.app)

    from src.controllers import auth as auth_controller

    app.register_blueprint(auth_controller.app)

    from src.controllers import role as role_controller

    app.register_blueprint(role_controller.app)

    return app


if __name__ == "__main__":
    # Cria e executa a aplicação Flask
    app = create_app()
    app.run(debug=True)
