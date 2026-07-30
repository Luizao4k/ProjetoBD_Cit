"""
Testes de integração do SqliteDiretorRepository (banco real em memória).
"""

import pytest

from domain.value_objects import Nome
from infrastructure.database.sqlite.repositories import (
    SqliteDreRepository,
    SqliteEscolaRepository,
    SqliteDiretorRepository,
)
from shared.exceptions import EscolaJaPossuiDiretorError, EscolaNaoEncontradaError
from shared.types import EscolaId
from tests.factories import DreFactory, EscolaFactory, DiretorFactory


@pytest.fixture
def escola_salva(conexao):
    dre = SqliteDreRepository(conexao).salvar(DreFactory.criar(id=None))
    return SqliteEscolaRepository(conexao).salvar(EscolaFactory.criar(id=None, dre_id=dre.id))


def test_salvar_atribui_id_e_persiste(conexao, escola_salva):
    repo = SqliteDiretorRepository(conexao)
    diretor = DiretorFactory.criar(id=None, escola_id=escola_salva.id)

    salvo = repo.salvar(diretor)

    assert salvo.id is not None
    encontrado = repo.buscar_por_id(salvo.id)
    assert encontrado is not None
    assert encontrado.email == salvo.email


def test_salvar_segunda_vez_para_mesma_escola_levanta_erro(conexao, escola_salva):
    repo = SqliteDiretorRepository(conexao)
    repo.salvar(DiretorFactory.criar(id=None, escola_id=escola_salva.id))

    with pytest.raises(EscolaJaPossuiDiretorError):
        repo.salvar(DiretorFactory.criar(id=None, escola_id=escola_salva.id))


def test_salvar_com_escola_inexistente_levanta_erro(conexao):
    repo = SqliteDiretorRepository(conexao)

    with pytest.raises(EscolaNaoEncontradaError):
        repo.salvar(DiretorFactory.criar(id=None, escola_id=EscolaId(999999)))


def test_buscar_por_escola(conexao, escola_salva):
    repo = SqliteDiretorRepository(conexao)
    salvo = repo.salvar(DiretorFactory.criar(id=None, escola_id=escola_salva.id))

    encontrado = repo.buscar_por_escola(escola_salva.id)

    assert encontrado is not None
    assert encontrado.id == salvo.id


def test_buscar_por_escola_sem_diretor_retorna_none(conexao, escola_salva):
    repo = SqliteDiretorRepository(conexao)
    assert repo.buscar_por_escola(escola_salva.id) is None


def test_atualizar_persiste_mudanca(conexao, escola_salva):
    repo = SqliteDiretorRepository(conexao)
    salvo = repo.salvar(DiretorFactory.criar(id=None, escola_id=escola_salva.id))

    salvo.nome = Nome("NOVO NOME")
    repo.atualizar(salvo)

    relido = repo.buscar_por_id(salvo.id)
    assert relido.nome.valor == "NOVO NOME"


def test_remover(conexao, escola_salva):
    repo = SqliteDiretorRepository(conexao)
    salvo = repo.salvar(DiretorFactory.criar(id=None, escola_id=escola_salva.id))

    repo.remover(salvo.id)

    assert repo.buscar_por_id(salvo.id) is None
