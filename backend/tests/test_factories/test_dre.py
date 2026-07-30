"""
Testes da DreFactory.
"""

from domain.entities import Dre
from domain.value_objects import Nome, Telefone
from shared.types import DreId

from tests.factories.dre_factory import DreFactory


def test_deve_criar_dre_valida():
    dre = DreFactory.criar()

    assert isinstance(dre, Dre)

    assert dre.id == DreId(1)
    assert dre.nome == Nome("DRE BELÉM")
    assert dre.telefone == Telefone("91999999999")


def test_deve_permitir_sobrescrever_campos():
    dre = DreFactory.criar(
        id=15,
        nome="DRE ALTAMIRA",
        telefone="91988888888",
    )

    assert dre.id == DreId(15)
    assert dre.nome == Nome("DRE ALTAMIRA")
    assert dre.telefone == Telefone("91988888888")


def test_deve_permitir_telefone_none():
    dre = DreFactory.criar(
        telefone=None
    )

    assert dre.telefone is None


def test_deve_permitir_id_none():
    dre = DreFactory.criar(
        id=None
    )

    assert dre.id is None
