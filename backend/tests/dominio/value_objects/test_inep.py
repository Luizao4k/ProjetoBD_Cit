import pytest

from domain.value_objects.inep import Inep
from shared.exceptions import InepInvalidoError


def test_deve_criar_inep_valido():
    inep = Inep("12345678")

    assert inep.valor == "12345678"


@pytest.mark.parametrize(
    "valor",
    [
        "",
        "123",
        "abcdefgh",
        "123456789",
        "1234abcd",
    ],
)
def test_inep_invalido(valor):
    with pytest.raises(InepInvalidoError):
        Inep(valor)
