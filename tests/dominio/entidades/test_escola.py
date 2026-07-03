import pytest

from time import sleep

from domain.entities import Escola
from domain.enums import TipoEscola
from domain.value_objects import Nome, Inep, Municipio, Endereco
from shared.types import EscolaId, DreId

@pytest.fixture
def escola():
    return Escola(
        id=EscolaId(1),
        inep=Inep("12345678"),
        nome=Nome("Escola A"),
        tipo=TipoEscola.ESTADUAL,
        municipio=Municipio("Belém"),
        dre_id=DreId(1),
        endereco=Endereco("Rua A"),
    )


def test_alterar_nome(escola):
    novo = Nome("Escola Nova")

    escola.alterar_nome(novo)

    assert escola.nome == novo


def test_alterar_endereco(escola):
    endereco = Endereco("Rua B")

    escola.alterar_endereco(endereco)

    assert escola.endereco == endereco


def test_remover_endereco(escola):
    escola.alterar_endereco(None)

    assert escola.endereco is None

def test_alterar_nome_atualiza_data(escola):
    atualizado_em = escola.atualizado_em

    sleep(0.01)

    escola.alterar_nome(Nome("Outra Escola"))

    assert escola.atualizado_em > atualizado_em
