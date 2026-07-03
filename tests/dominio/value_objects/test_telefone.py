import pytest

from domain.value_objects.telefone import Telefone
from shared.exceptions import TelefoneInvalidoError


def test_deve_remover_caracteres():
    telefone = Telefone("(91) 99999-9999")

    assert telefone.valor == "91999999999"


def test_telefone_invalido():
    with pytest.raises(TelefoneInvalidoError):
        Telefone("123")


def test_criar_none():
    assert Telefone.criar(None) is None


def test_criar_invalido():
    assert Telefone.criar("12") is None


def test_criar_valido():
    telefone = Telefone.criar("(91)99999-9999")
    assert telefone is not None
    assert telefone.valor == "91999999999"
