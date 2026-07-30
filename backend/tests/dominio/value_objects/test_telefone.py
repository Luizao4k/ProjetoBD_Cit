import pytest

from domain.value_objects.telefone import Telefone
from shared.exceptions import TelefoneInvalidoError


def test_deve_remover_caracteres():
    telefone = Telefone("(91) 99999-9999")

    assert telefone.valor == "91999999999"


def test_telefone_invalido():
    with pytest.raises(TelefoneInvalidoError):
        Telefone("123")
