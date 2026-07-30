"""
Testes de integração do SqliteTurmaCemepRepository (banco real em memória).
"""

import pytest

from domain.value_objects import Nome
from infrastructure.database.sqlite.repositories import (
    SqliteDreRepository,
    SqliteEscolaRepository,
    SqliteCemepRepository,
    SqliteResponsavelRepository,
    SqliteTurmaCemepRepository,
)
from shared.exceptions import ResponsavelNaoEncontradoError
from shared.types import ResponsavelId
from tests.factories import (
    DreFactory,
    EscolaFactory,
    CemepFactory,
    ResponsavelFactory,
    TurmaCemepFactory,
)


@pytest.fixture
def responsavel_salvo(conexao):
    dre = SqliteDreRepository(conexao).salvar(DreFactory.criar(id=None))
    escola = SqliteEscolaRepository(conexao).salvar(EscolaFactory.criar(id=None, dre_id=dre.id))
    cemep = SqliteCemepRepository(conexao).salvar(CemepFactory.criar(id=None, escola_id=escola.id))
    return SqliteResponsavelRepository(conexao).salvar(ResponsavelFactory.criar(id=None, cemep_id=cemep.id))


def test_salvar_atribui_id_e_persiste(conexao, responsavel_salvo):
    repo = SqliteTurmaCemepRepository(conexao)
    salvo = repo.salvar(TurmaCemepFactory.criar(id=None, responsavel_id=responsavel_salvo.id))

    assert salvo.id is not None
    encontrado = repo.buscar_por_id(salvo.id)
    assert encontrado is not None
    assert encontrado.nome_turma == salvo.nome_turma


def test_salvar_com_responsavel_inexistente_levanta_erro(conexao):
    repo = SqliteTurmaCemepRepository(conexao)

    with pytest.raises(ResponsavelNaoEncontradoError):
        repo.salvar(TurmaCemepFactory.criar(id=None, responsavel_id=ResponsavelId(999999)))


def test_buscar_por_responsavel(conexao, responsavel_salvo):
    repo = SqliteTurmaCemepRepository(conexao)
    repo.salvar(TurmaCemepFactory.criar(id=None, responsavel_id=responsavel_salvo.id, nome_turma="TURMA A"))
    repo.salvar(TurmaCemepFactory.criar(id=None, responsavel_id=responsavel_salvo.id, nome_turma="TURMA B"))

    encontradas = repo.buscar_por_responsavel(responsavel_salvo.id)

    assert len(encontradas) == 2


def test_atualizar_persiste_mudanca(conexao, responsavel_salvo):
    repo = SqliteTurmaCemepRepository(conexao)
    salvo = repo.salvar(TurmaCemepFactory.criar(id=None, responsavel_id=responsavel_salvo.id))

    salvo.nome_turma = Nome("TURMA RENOMEADA")
    repo.atualizar(salvo)

    relido = repo.buscar_por_id(salvo.id)
    assert relido.nome_turma.valor == "TURMA RENOMEADA"


def test_remover(conexao, responsavel_salvo):
    repo = SqliteTurmaCemepRepository(conexao)
    salvo = repo.salvar(TurmaCemepFactory.criar(id=None, responsavel_id=responsavel_salvo.id))

    repo.remover(salvo.id)

    assert repo.buscar_por_id(salvo.id) is None
