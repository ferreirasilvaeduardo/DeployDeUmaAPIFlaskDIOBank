import os

from flask import Flask, json
from werkzeug.exceptions import HTTPException

from src.config import Config
from src.models import bcrypt, db, jwt, ma, migrate, spec


def create_app(
    environment=os.getenv("ENVIRONMENT"),
):
    """
    Cria e configura a aplicação Flask.
    """
    app = Flask(__name__, instance_relative_config=True)

    if not environment:
        raise ValueError(
            "A variável de ambiente ENVIRONMENT não foi definida.", str(environment)
        )
    else:
        environment = str(environment).strip().lower()

    if environment not in ["development", "testing", "production"]:
        raise ValueError(
            "A variável de ambiente ENVIRONMENT deve ser 'development', 'testing' ou 'production'."
        )

    app.config.from_object(f"src.config.{str(environment).strip().title()}Config")

    # Verifica se a variável instance_path existe no objeto app
    if hasattr(app, "instance_path"):
        os.makedirs(app.instance_path, exist_ok=True)
    else:
        raise AttributeError("O objeto app não possui a variável instance_path.")

    # Inicializa a configuração da aplicação
    Config.init_app(app)

    # Inicializa a aplicação com a extensão SQLAlchemy
    db.init_app(app)
    # Inicializa a aplicação com a extensão Flask-Migrate
    migrate.init_app(app, db)
    # Inicializa a aplicação com a extensão Flask-JWT-Extended
    jwt.init_app(app)
    # Inicializa a aplicação com a extensão Flask-Bcrypt
    bcrypt.init_app(app)
    # Inicializa a aplicação com a extensão Flask-Marshmallow
    ma.init_app(app)

    # Importa e registra blueprints para os controladores
    from src.controllers import auth as controllers_app_auth
    from src.controllers import post as controllers_app_post
    from src.controllers import role as controllers_app_role
    from src.controllers import user as controllers_app_user

    app.register_blueprint(controllers_app_user.app)
    app.register_blueprint(controllers_app_role.app)
    app.register_blueprint(controllers_app_post.app)
    app.register_blueprint(controllers_app_auth.app)

    # Define uma rota simples que retorna uma mensagem de boas-vindas
    @app.route("/")  # @app.route("/docs/")
    def home():
        """Retorna uma mensagem de boas-vindas."""
        return spec.path(view=controllers_app_user.get_user).to_dict()  # "Olá, Seja bem vindo!"

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        response = e.get_response()
        response.data = json.dumps(
            {
                "code": e.code,
                "name": e.name,
                "description": e.description,
            }
        )
        response.content_type = "application/json"
        return response

    return app


if __name__ == "__main__":
    # Cria e executa a aplicação Flask
    app = create_app(environment=os.getenv("ENVIRONMENT"))
    app.run(debug=True)

# export ENVIRONMENT="sqlite:///blog.sqlite"
##
# ProductionConfig
# export ENVIRONMENT="production"
# --> ENVIRONMENT=production poetry run flask --app src.app run
##
# DevelopmentConfig:
# export ENVIRONMENT="development"
# --> ENVIRONMENT=development poetry run flask --app src.app run --debug
##
# class TestingConfig(Config):
# export ENVIRONMENT="testing"
# --> ENVIRONMENT=testing poetry run flask --app src.app run --debug
