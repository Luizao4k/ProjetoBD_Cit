import pytest

from time import sleep

from domain.entities import Diretor
from domain.value_objects import Nome, Email, Telefone
from shared.types import DiretorId, EscolaId

@pytest.fixture
def diretor():
    return Diretor(
        id=DiretorId(1),
        escola_id=EscolaId(10),
        nome=Nome("Carlos"),
        telefone=Telefone("91999999999"),
        email=Email("carlos@email.com"),
    )


def test_alterar_nome(diretor):
    nome = Nome("João")

    diretor.alterar_nome(nome)

    assert diretor.nome == nome


def test_alterar_email(diretor):
    email = Email("joao@email.com")

    diretor.alterar_email(email)

    assert diretor.email == email


def test_alterar_telefone(diretor):
    telefone = Telefone("91988888888")

    diretor.alterar_telefone(telefone)

    assert diretor.telefone == telefone

