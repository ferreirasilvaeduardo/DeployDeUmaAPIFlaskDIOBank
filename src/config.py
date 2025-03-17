import logging
import os


class Config(object):
    """
    Configurações base para a aplicação.
    """

    DEBUG = False  # Não ativa o modo de depuração, pois é inseguro, o correto é ativar apenas em ambiente de desenvolvimento passando como parametro --debug
    TESTING = False
    SECRET_KEY = os.getenv(
        "SECRET_KEY", "default-secret-key"
    )  # Chave secreta para a aplicação
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///blog.sqlite"
    )  # URI do banco de dados
    SQLALCHEMY_TRACK_MODIFICATIONS = (
        False  # Desativa track modifications para economizar recursos
    )
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY", "default-jwt-secret-key"
    )  # Chave secreta para JWT
    PRESERVE_CONTEXT_ON_EXCEPTION = (
        False  # Desativa a preservação do contexto em caso de exceção
    )
    SQLALCHEMY_ECHO = False  # Desativa a saída de depuração do SQLAlchemy

    # Configuração de logging
    LOG_LEVEL = logging.INFO  # Nível de log padrão
    LOG_FORMAT = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # Formato do log
    )
    LOG_FILE = "app.log"  # Arquivo de log padrão

    @staticmethod
    def init_app(app):
        """
        Inicializa a configuração da aplicação.
        """
        # Configura o logger
        handler = logging.StreamHandler()
        handler.setLevel(app.config["LOG_LEVEL"])
        formatter = logging.Formatter(app.config["LOG_FORMAT"])
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)

        # Configura o log para arquivo se especificado
        if app.config["LOG_FILE"]:
            file_handler = logging.FileHandler(app.config["LOG_FILE"])
            file_handler.setLevel(app.config["LOG_LEVEL"])
            file_handler.setFormatter(formatter)
            app.logger.addHandler(file_handler)


class ProductionConfig(Config):
    """
    Configurações específicas para o ambiente de produção.
    """

    LOG_LEVEL = logging.WARNING  # Nível de log para produção
    LOG_FILE = "production.log"  # Arquivo de log para produção


class DevelopmentConfig(Config):
    """
    Configurações específicas para o ambiente de desenvolvimento.
    """

    DEBUG = True  # Não ativa o modo de depuração, pois é inseguro, o correto é ativar apenas em ambiente de desenvolvimento passando como parametro --debug
    SECRET_KEY = os.getenv(
        "DEV_SECRET_KEY", "dev-secret-key"
    )  # Chave secreta para desenvolvimento
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DEV_DATABASE_URL", "sqlite:///blog.sqlite"
    )  # URI do banco de dados para desenvolvimento
    SQLALCHEMY_TRACK_MODIFICATIONS = (
        True  # Ativa track modifications para desenvolvimento
    )
    JWT_SECRET_KEY = os.getenv(
        "DEV_JWT_SECRET_KEY", "dev-jwt-secret-key"
    )  # Chave secreta para JWT em desenvolvimento
    PRESERVE_CONTEXT_ON_EXCEPTION = (
        True  # Ativa a preservação do contexto em caso de exceção para depuração
    )
    SQLALCHEMY_ECHO = True  # Ativa a saída de depuração do SQLAlchemy
    LOG_LEVEL = logging.DEBUG  # Nível de log para desenvolvimento
    LOG_FILE = "development.log"  # Arquivo de log para desenvolvimento


class TestingConfig(Config):
    """
    Configurações específicas para o ambiente de testes.
    """

    DEBUG = True  # Não ativa o modo de depuração, pois é inseguro, o correto é ativar apenas em ambiente de desenvolvimento passando como parametro --debug
    TESTING = True
    SECRET_KEY = os.getenv(
        "TEST_SECRET_KEY", "test-secret-key"
    )  # Chave secreta para testes
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TEST_DATABASE_URL", "sqlite:///:memory:"
    )  # URI do banco de dados para testes
    JWT_SECRET_KEY = os.getenv(
        "TEST_JWT_SECRET_KEY", "test-jwt-secret-key"
    )  # Chave secreta para JWT em testes
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # Ativa track modifications para testes
    PRESERVE_CONTEXT_ON_EXCEPTION = (
        False  # Desativa a preservação do contexto em caso de exceção
    )
    SQLALCHEMY_ECHO = True  # Ativa a saída de depuração do SQLAlchemy para testes
    LOG_LEVEL = logging.DEBUG  # Nível de log para testes
    LOG_FILE = "testing.log"  # Arquivo de log para testes
