"""
Testes de integração do SqliteStarlinkRepository (banco real em memória).
"""

import pytest

from domain.value_objects import Nome
from infrastructure.database.sqlite.repositories import (
    SqliteDreRepository,
    SqliteEscolaRepository,
    SqliteStarlinkRepository,
)
from shared.exceptions import EscolaNaoEncontradaError
from shared.types import EscolaId
from tests.factories import DreFactory, EscolaFactory, StarlinkFactory


@pytest.fixture
def escola_salva(conexao):
    dre = SqliteDreRepository(conexao).salvar(DreFactory.criar(id=None))
    return SqliteEscolaRepository(conexao).salvar(EscolaFactory.criar(id=None, dre_id=dre.id))


def test_salvar_atribui_id_e_persiste(conexao, escola_salva):
    repo = SqliteStarlinkRepository(conexao)
    salvo = repo.salvar(StarlinkFactory.criar(id=None, escola_id=escola_salva.id))

    assert salvo.id is not None
    encontrado = repo.buscar_por_id(salvo.id)
    assert encontrado is not None
    assert encontrado.designacao == salvo.designacao


def test_salvar_com_escola_inexistente_levanta_erro(conexao):
    repo = SqliteStarlinkRepository(conexao)

    with pytest.raises(EscolaNaoEncontradaError):
        repo.salvar(StarlinkFactory.criar(id=None, escola_id=EscolaId(999999)))


def test_varios_starlinks_para_a_mesma_escola_e_permitido(conexao, escola_salva):
    repo = SqliteStarlinkRepository(conexao)
    repo.salvar(StarlinkFactory.criar(id=None, escola_id=escola_salva.id, designacao="KIT 1"))
    repo.salvar(StarlinkFactory.criar(id=None, escola_id=escola_salva.id, designacao="KIT 2"))

    encontrados = repo.buscar_por_escola(escola_salva.id)

    assert len(encontrados) == 2


def test_atualizar_persiste_mudanca(conexao, escola_salva):
    repo = SqliteStarlinkRepository(conexao)
    salvo = repo.salvar(StarlinkFactory.criar(id=None, escola_id=escola_salva.id))

    salvo.designacao = Nome("KIT RENOMEADO")
    repo.atualizar(salvo)

    relido = repo.buscar_por_id(salvo.id)
    assert relido.designacao.valor == "KIT RENOMEADO"


def test_remover(conexao, escola_salva):
    repo = SqliteStarlinkRepository(conexao)
    salvo = repo.salvar(StarlinkFactory.criar(id=None, escola_id=escola_salva.id))

    repo.remover(salvo.id)

    assert repo.buscar_por_id(salvo.id) is None
