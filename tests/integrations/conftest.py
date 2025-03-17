import pytest

from src.models import Role, User, create_app, db


@pytest.fixture(
    scope="function"
)  # scope= default:function, module, class, function, package or session
def app():

    app = create_app(environment="testing")
    # app = create_app(
    #     {
    #         "SECRET_KEY": "test",
    #         "SQLALCHEMY_DATABASE_URI": "sqlite://",  # Configura o banco de dados em memória
    #         "JWT_SECRET_KEY": "test",
    #     }
    # )

    with app.app_context():
        db.create_all()
        yield app
        # db.session.rollback()
        db.drop_all()

    # clean up / reset resources here


@pytest.fixture
def client(app):
    return app.test_client()


# @pytest.fixture()
# def runner(app):
#     return app.test_cli_runner()


@pytest.fixture()
def access_token(client):
    # given
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()
    user = User(username="john-doe", password="test", role_id=role.id)
    db.session.add(user)
    db.session.commit()
    response = client.post(
        "/auth/login", json={"username": user.username, "password": user.password}
    )
    return response.json["access_token"]
