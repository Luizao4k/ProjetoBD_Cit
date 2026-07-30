"""
Testes da ResponsavelFactory.
"""

from domain.entities import Responsavel
from domain.value_objects import Nome
from shared.types import ResponsavelId, CemepId

from tests.factories.responsavel_factory import ResponsavelFactory

def test_deve_criar_responsavel_valido():
    responsavel = ResponsavelFactory.criar()

    assert isinstance(responsavel, Responsavel)

    assert responsavel.id == ResponsavelId(1)
    assert responsavel.nome == Nome("JOÃO RESPONSÁVEL")
    assert responsavel.cemep_id == CemepId(1)


def test_deve_permitir_sobrescrever_campos():
    responsavel = ResponsavelFactory.criar(
        id=10,
        nome="MARIA RESPONSÁVEL",
        cemep_id=5,
    )

    assert responsavel.id == ResponsavelId(10)
    assert responsavel.nome == Nome("MARIA RESPONSÁVEL")
    assert responsavel.cemep_id == CemepId(5)


def test_deve_permitir_id_none():
    responsavel = ResponsavelFactory.criar(id=None)

    assert responsavel.id is None