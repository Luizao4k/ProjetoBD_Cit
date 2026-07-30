"""
Testes de integração do SqliteCemepRepository (banco real em memória).
"""

import pytest

from domain.value_objects import Comentario
from infrastructure.database.sqlite.repositories import (
    SqliteDreRepository,
    SqliteEscolaRepository,
    SqliteCemepRepository,
    SqliteResponsavelRepository,
)
from shared.exceptions import (
    EscolaJaPossuiCemepError,
    EscolaNaoEncontradaError,
    CemepPossuiResponsaveisError,
)
from shared.types import EscolaId
from tests.factories import DreFactory, EscolaFactory, CemepFactory, ResponsavelFactory


@pytest.fixture
def escola_salva(conexao):
    dre = SqliteDreRepository(conexao).salvar(DreFactory.criar(id=None))
    return SqliteEscolaRepository(conexao).salvar(EscolaFactory.criar(id=None, dre_id=dre.id))


def test_salvar_atribui_id_e_persiste(conexao, escola_salva):
    repo = SqliteCemepRepository(conexao)
    salvo = repo.salvar(CemepFactory.criar(id=None, escola_id=escola_salva.id))

    assert salvo.id is not None
    encontrado = repo.buscar_por_id(salvo.id)
    assert encontrado is not None
    assert encontrado.comentario == salvo.comentario


def test_salvar_segunda_vez_para_mesma_escola_levanta_erro(conexao, escola_salva):
    repo = SqliteCemepRepository(conexao)
    repo.salvar(CemepFactory.criar(id=None, escola_id=escola_salva.id))

    with pytest.raises(EscolaJaPossuiCemepError):
        repo.salvar(CemepFactory.criar(id=None, escola_id=escola_salva.id))


def test_salvar_com_escola_inexistente_levanta_erro(conexao):
    repo = SqliteCemepRepository(conexao)

    with pytest.raises(EscolaNaoEncontradaError):
        repo.salvar(CemepFactory.criar(id=None, escola_id=EscolaId(999999)))


def test_buscar_por_escola(conexao, escola_salva):
    repo = SqliteCemepRepository(conexao)
    salvo = repo.salvar(CemepFactory.criar(id=None, escola_id=escola_salva.id))

    encontrado = repo.buscar_por_escola(escola_salva.id)

    assert encontrado is not None
    assert encontrado.id == salvo.id


def test_atualizar_persiste_comentario(conexao, escola_salva):
    repo = SqliteCemepRepository(conexao)
    salvo = repo.salvar(CemepFactory.criar(id=None, escola_id=escola_salva.id))

    salvo.comentario = Comentario("comentário atualizado")
    repo.atualizar(salvo)

    relido = repo.buscar_por_id(salvo.id)
    assert relido.comentario.valor == "comentário atualizado"


def test_remover_sem_responsaveis(conexao, escola_salva):
    repo = SqliteCemepRepository(conexao)
    salvo = repo.salvar(CemepFactory.criar(id=None, escola_id=escola_salva.id))

    repo.remover(salvo.id)

    assert repo.buscar_por_id(salvo.id) is None


def test_remover_bloqueado_por_responsavel(conexao, escola_salva):
    repo_cemep = SqliteCemepRepository(conexao)
    cemep = repo_cemep.salvar(CemepFactory.criar(id=None, escola_id=escola_salva.id))
    SqliteResponsavelRepository(conexao).salvar(ResponsavelFactory.criar(id=None, cemep_id=cemep.id))

    with pytest.raises(CemepPossuiResponsaveisError):
        repo_cemep.remover(cemep.id)
