from http import HTTPStatus  # Importa os códigos de status HTTP
from unittest.mock import Mock, patch

from src.utils.utils import requires_role, requires_role_name


def test_requeris_role_name_true():
    """
    Testa a função requeris_role com um usuário que possui a role.
    Verifica se a função retorna True
    """
    mock_user = Mock()
    mock_user.role.name = "admin"
    with patch("src.utils.utils.get_jwt_identity"), patch(
        "src.utils.utils.db.get_or_404", return_value=mock_user
    ):
        decorated_function = requires_role_name("admin")(lambda: "success")
        assert decorated_function() == "success"
    # mock_get_jwt_identity = patch("src.utils.utils.get_jwt_identity")
    # mock_db_get_or_404 = patch("src.utils.utils.db.get_or_404", return_value=mock_user)
    # mock_get_jwt_identity.start()
    # mock_db_get_or_404.start()
    # decorated_function = requires_role_name("admin")(lambda: "success")
    # result = decorated_function()
    # assert result == "success"
    # mock_get_jwt_identity.stop()
    # mock_db_get_or_404.stop()


def test_requeris_role_name_false():
    """
    Testa a função requeris_role com um usuário que possui a role.
    Verifica se a função retorna False
    """
    mock_user = Mock()
    mock_user.role.name = "user"
    with patch("src.utils.utils.get_jwt_identity"), patch(
        "src.utils.utils.db.get_or_404", return_value=mock_user
    ):
        decorated_function = requires_role_name("admin")(lambda: "success")
        assert decorated_function() == (
            {"msg": "Usuário não tem permissão!"},
            HTTPStatus.FORBIDDEN,
        )
    # mock_get_jwt_identity = patch("src.utils.utils.get_jwt_identity")
    # mock_db_get_or_404 = patch("src.utils.utils.db.get_or_404", return_value=mock_user)
    # mock_get_jwt_identity.start()
    # mock_db_get_or_404.start()
    # decorated_function = requires_role_name("admin")(lambda: "success")
    # result = decorated_function()
    # assert result == ({"msg": "Usuário não tem permissão!"}, HTTPStatus.FORBIDDEN)
    # mock_get_jwt_identity.stop()
    # mock_db_get_or_404.stop()


def test_requeris_role_true(mocker):
    mock_user = mocker.Mock()
    mock_user.role.id = 1
    mocker.patch("src.utils.utils.get_jwt_identity")
    mocker.patch("src.utils.utils.db.get_or_404", return_value=mock_user)
    # when
    decorated_function = requires_role(1)(lambda: "success")
    # True
    assert decorated_function() == "success"


def test_requeris_role_false(mocker):
    mock_user = mocker.Mock()
    mock_user.role.id = 2
    mocker.patch("src.utils.utils.get_jwt_identity")
    mocker.patch("src.utils.utils.db.get_or_404", return_value=mock_user)
    # when
    decorated_function = requires_role(1)(lambda: "success")
    # True
    assert decorated_function() == (
        {"msg": "Usuário não tem permissão!"},
        HTTPStatus.FORBIDDEN,
    )
