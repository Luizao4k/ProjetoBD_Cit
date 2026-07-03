import pytest

from typing import cast
from domain.value_objects.quantidade import Quantidade
from shared.exceptions import ValorInvalidoError


def test_quantidade_valida():
    quantidade = Quantidade(10)

    assert quantidade.valor == 10


@pytest.mark.parametrize(
    "valor",
    [
        0,
        -1,
        -20,
    ],
)
def test_quantidade_nao_pode_ser_menor_ou_igual_zero(valor):
    with pytest.raises(ValorInvalidoError):
        Quantidade(valor)


def test_quantidade_deve_ser_inteiro():
    with pytest.raises(ValorInvalidoError):
        Quantidade(cast(int, 10.5)) 
