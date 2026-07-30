"""
Testes de integração do SqliteChromebookRepository (banco real em memória).
"""

import pytest

from domain.value_objects import Quantidade
from infrastructure.database.sqlite.repositories import (
    SqliteDreRepository,
    SqliteEscolaRepository,
    SqliteChromebookRepository,
)
from shared.exceptions import EscolaJaPossuiChromebookError, EscolaNaoEncontradaError
from shared.types import EscolaId
from tests.factories import DreFactory, EscolaFactory, ChromebookFactory


@pytest.fixture
def escola_salva(conexao):
    dre = SqliteDreRepository(conexao).salvar(DreFactory.criar(id=None))
    return SqliteEscolaRepository(conexao).salvar(EscolaFactory.criar(id=None, dre_id=dre.id))


def test_salvar_atribui_id_e_persiste(conexao, escola_salva):
    repo = SqliteChromebookRepository(conexao)
    salvo = repo.salvar(ChromebookFactory.criar(id=None, escola_id=escola_salva.id))

    assert salvo.id is not None
    encontrado = repo.buscar_por_id(salvo.id)
    assert encontrado is not None
    assert int(encontrado.kit_aluno) == int(salvo.kit_aluno)


def test_salvar_com_kits_nulos(conexao, escola_salva):
    repo = SqliteChromebookRepository(conexao)
    salvo = repo.salvar(
        ChromebookFactory.criar(id=None, escola_id=escola_salva.id, kit_aluno=None, kit_professor=None)
    )

    encontrado = repo.buscar_por_id(salvo.id)
    assert encontrado.kit_aluno is None
    assert encontrado.kit_professor is None


def test_salvar_segunda_vez_para_mesma_escola_levanta_erro(conexao, escola_salva):
    repo = SqliteChromebookRepository(conexao)
    repo.salvar(ChromebookFactory.criar(id=None, escola_id=escola_salva.id))

    with pytest.raises(EscolaJaPossuiChromebookError):
        repo.salvar(ChromebookFactory.criar(id=None, escola_id=escola_salva.id))


def test_salvar_com_escola_inexistente_levanta_erro(conexao):
    repo = SqliteChromebookRepository(conexao)

    with pytest.raises(EscolaNaoEncontradaError):
        repo.salvar(ChromebookFactory.criar(id=None, escola_id=EscolaId(999999)))


def test_buscar_por_escola(conexao, escola_salva):
    repo = SqliteChromebookRepository(conexao)
    salvo = repo.salvar(ChromebookFactory.criar(id=None, escola_id=escola_salva.id))

    encontrado = repo.buscar_por_escola(escola_salva.id)

    assert encontrado is not None
    assert encontrado.id == salvo.id


def test_atualizar_persiste_novas_quantidades(conexao, escola_salva):
    repo = SqliteChromebookRepository(conexao)
    salvo = repo.salvar(ChromebookFactory.criar(id=None, escola_id=escola_salva.id))

    salvo.kit_aluno = Quantidade(99)
    repo.atualizar(salvo)

    relido = repo.buscar_por_id(salvo.id)
    assert int(relido.kit_aluno) == 99


def test_remover(conexao, escola_salva):
    repo = SqliteChromebookRepository(conexao)
    salvo = repo.salvar(ChromebookFactory.criar(id=None, escola_id=escola_salva.id))

    repo.remover(salvo.id)

    assert repo.buscar_por_id(salvo.id) is None
