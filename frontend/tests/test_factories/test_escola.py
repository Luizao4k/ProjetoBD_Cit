"""
Testes da EscolaFactory.
"""

from domain.entities import Escola
from domain.enums import TipoEscola
from domain.value_objects import Endereco, Inep, Municipio, Nome
from shared.types import DreId, EscolaId

from tests.factories.escola_factory import EscolaFactory


def test_deve_criar_escola_valida():
    escola = EscolaFactory.criar()

    assert isinstance(escola, Escola)

    assert escola.id == EscolaId(1)
    assert escola.inep == Inep("15000000")
    assert escola.nome == Nome("ESCOLA TESTE")
    assert escola.tipo == TipoEscola.ESTADUAL
    assert escola.municipio == Municipio("BELÉM")
    assert escola.dre_id == DreId(1)
    assert escola.endereco is None


def test_deve_permitir_sobrescrever_campos():
    escola = EscolaFactory.criar(
        id=10,
        inep="15001234",
        nome="ESCOLA NOVA",
        tipo=TipoEscola.MUNICIPAL,
        municipio="ANANINDEUA",
        dre_id=5,
        endereco="Rua A, nº 100",
    )

    assert escola.id == EscolaId(10)
    assert escola.inep == Inep("15001234")
    assert escola.nome == Nome("ESCOLA NOVA")
    assert escola.tipo == TipoEscola.MUNICIPAL
    assert escola.municipio == Municipio("ANANINDEUA")
    assert escola.dre_id == DreId(5)
    assert escola.endereco == Endereco("Rua A, nº 100")


def test_deve_permitir_endereco_none():
    escola = EscolaFactory.criar(endereco=None)

    assert escola.endereco is None


def test_deve_permitir_id_none():
    escola = EscolaFactory.criar(id=None)

    assert escola.id is None
