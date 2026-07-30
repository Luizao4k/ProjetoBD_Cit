import pytest

from time import sleep

from domain.entities import Dre
from domain.value_objects import Nome, Telefone
from shared.types import DreId

@pytest.fixture
def dre():
    return Dre(
        id=DreId(1),
        nome=Nome("DRE Belém"),
        telefone=Telefone("91999999999"),
    )


def test_alterar_nome(dre):
    novo = Nome("DRE Ananindeua")

    dre.alterar_nome(novo)

    assert dre.nome == novo


def test_alterar_telefone(dre):
    telefone = Telefone("91988888888")

    dre.alterar_telefone(telefone)

    assert dre.telefone == telefone

def test_alterar_nome_atualiza_data(escola):
    atualizado_em = escola.atualizado_em

    sleep(0.01)

    escola.alterar_nome(Nome("Outra Escola"))

    assert escola.atualizado_em > atualizado_em
