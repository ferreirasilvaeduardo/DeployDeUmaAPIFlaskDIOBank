from flask_sqlalchemy import SQLAlchemy  # Importa SQLAlchemy do Flask

db = SQLAlchemy()  # Cria uma instância de SQLAlchemy


def init_app(app):
    """
    Inicializa o banco de dados com a aplicação Flask fornecida.

    :param app: Instância da aplicação Flask
    """
    db.init_app(app)  # Inicializa a instância do banco de dados com a aplicação Flask
    with app.app_context():
        db.create_all()  # Cria todas as tabelas no banco de dados
