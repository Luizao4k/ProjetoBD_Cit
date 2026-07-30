import pytest

from time import sleep

from domain.entities import Responsavel, escola
from domain.value_objects import Nome
from shared.types import ResponsavelId, CemepId

@pytest.fixture
def responsavel():
    return Responsavel(
        id=ResponsavelId(1),
        nome=Nome("Maria"),
        cemep_id=CemepId(2),
    )


def test_alterar_nome(responsavel):
    nome = Nome("Ana")

    responsavel.alterar_nome(nome)

    assert responsavel.nome == nome
