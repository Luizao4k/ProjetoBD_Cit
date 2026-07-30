"""
Testes da DiretorFactory.
"""

from domain.entities import Diretor
from domain.value_objects import Nome, Telefone, Email
from shared.types import DiretorId, EscolaId

from tests.factories.diretor_factory import DiretorFactory


def test_deve_criar_diretor_valido():
    diretor = DiretorFactory.criar()

    assert isinstance(diretor, Diretor)

    assert diretor.id == DiretorId(1)
    assert diretor.escola_id == EscolaId(1)
    assert diretor.nome == Nome("JOÃO DA SILVA")
    assert diretor.telefone == Telefone("91999999999")
    assert diretor.email == Email("joao@email.com")


def test_deve_permitir_sobrescrever_campos():
    diretor = DiretorFactory.criar(
        id=10,
        escola_id=25,
        nome="MARIA SILVA",
        telefone="91988888888",
        email="maria@email.com",
    )

    assert diretor.id == DiretorId(10)
    assert diretor.escola_id == EscolaId(25)
    assert diretor.nome == Nome("MARIA SILVA")
    assert diretor.telefone == Telefone("91988888888")
    assert diretor.email == Email("maria@email.com")


def test_deve_permitir_email_none():
    diretor = DiretorFactory.criar(email=None)

    assert diretor.email is None


def test_deve_permitir_telefone_none():
    diretor = DiretorFactory.criar(telefone=None)

    assert diretor.telefone is None


def test_deve_permitir_id_none():
    diretor = DiretorFactory.criar(id=None)

    assert diretor.id is None
