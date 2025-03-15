import pytest

from src.utils.utils import eleva_quadrado


def test_eleva_quadrado_with_negative_number():
    """
    Testa a função eleva_quadrado com um número negativo.
    Verifica se o quadrado de -3 é 9.
    """
    result = eleva_quadrado(-3)
    assert result == 9, "Expected -3 squared to be 9"


def test_eleva_quadrado_with_zero():
    """
    Testa a função eleva_quadrado com zero.
    Verifica se o quadrado de 0 é 0.
    """
    result = eleva_quadrado(0)
    assert result == 0, "Expected 0 squared to be 0"


def test_eleva_quadrado_with_large_number():
    """
    Testa a função eleva_quadrado com um número grande.
    Verifica se o quadrado de 1000 é 1000000.
    """
    result = eleva_quadrado(1000)
    assert result == 1000000, "Expected 1000 squared to be 1000000"


def test_eleva_quadrado_with_float():
    """
    Testa a função eleva_quadrado com um número de ponto flutuante.
    Verifica se o quadrado de 2.5 é 6.25.
    """
    result = eleva_quadrado(2.5)
    assert result == 6.25, "Expected 2.5 squared to be 6.25"


def test_eleva_quadrado_with_string():
    """
    Testa a função eleva_quadrado com uma string.
    Verifica se a função levanta um TypeError.
    """
    with pytest.raises(TypeError):
        eleva_quadrado("string")


def test_eleva_quadrado_sucesso():
    resultado = eleva_quadrado(2)
    assert resultado == 4


@pytest.mark.parametrize("test_input,expected", [(2, 4), (3, 9), (4, 16)])
def test_eleva_quadrado_sucesso_01(test_input, expected):
    resultado = eleva_quadrado(test_input)
    assert resultado == expected


def test_eleva_quadrado_falha():
    with pytest.raises(TypeError) as excinfo:
        eleva_quadrado("a")
    assert "unsupported operand type(s) for ** or pow()" in str(excinfo.value)


@pytest.mark.parametrize("test_input,expected", [(3, 6), (4, 8), (5, 24)])
def test_eleva_quadrado_falha_01(test_input, expected):
    resultado = eleva_quadrado(test_input)
    assert resultado != expected


@pytest.mark.parametrize(
    "test_input, exc_class, msg",
    [
        ("a", TypeError, "unsupported operand type(s) for ** or pow()"),
        (None, TypeError, "unsupported operand type(s) for ** or pow()"),
    ],
)
def test_eleva_quadrado_falha_02(test_input, exc_class, msg):
    with pytest.raises(exc_class) as excinfo:
        eleva_quadrado(test_input)
    assert msg in str(excinfo.value)
