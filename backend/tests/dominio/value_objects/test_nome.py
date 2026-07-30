import pytest

from domain.value_objects.nome import Nome
from shared.exceptions import NomeInvalidoError


def test_deve_criar_nome_valido():
    nome = Nome(" João Silva ")

    assert nome.valor == "JOAO SILVA"


def test_deve_remover_acentos():
    nome = Nome("José")

    assert nome.valor == "JOSE"


def test_deve_lancar_erro_nome_vazio():
    with pytest.raises(NomeInvalidoError):
        Nome("")


def test_deve_lancar_erro_nome_so_com_espacos():
    with pytest.raises(NomeInvalidoError):
        Nome("     ")


def test_str_retorna_valor():
    nome = Nome("Maria")

    assert str(nome) == "MARIA"
