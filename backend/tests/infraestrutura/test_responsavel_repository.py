"""
Testes de integração do SqliteResponsavelRepository (banco real em memória).
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
from shared.exceptions import CemepNaoEncontradoError, ResponsavelPossuiTurmasError
from shared.types import CemepId
from tests.factories import (
    DreFactory,
    EscolaFactory,
    CemepFactory,
    ResponsavelFactory,
    TurmaCemepFactory,
)


@pytest.fixture
def cemep_salvo(conexao):
    dre = SqliteDreRepository(conexao).salvar(DreFactory.criar(id=None))
    escola = SqliteEscolaRepository(conexao).salvar(EscolaFactory.criar(id=None, dre_id=dre.id))
    return SqliteCemepRepository(conexao).salvar(CemepFactory.criar(id=None, escola_id=escola.id))


def test_salvar_atribui_id_e_persiste(conexao, cemep_salvo):
    repo = SqliteResponsavelRepository(conexao)
    salvo = repo.salvar(ResponsavelFactory.criar(id=None, cemep_id=cemep_salvo.id))

    assert salvo.id is not None
    encontrado = repo.buscar_por_id(salvo.id)
    assert encontrado is not None
    assert encontrado.nome == salvo.nome


def test_salvar_com_cemep_inexistente_levanta_erro(conexao):
    repo = SqliteResponsavelRepository(conexao)

    with pytest.raises(CemepNaoEncontradoError):
        repo.salvar(ResponsavelFactory.criar(id=None, cemep_id=CemepId(999999)))


def test_varios_responsaveis_para_o_mesmo_cemep_e_permitido(conexao, cemep_salvo):
    repo = SqliteResponsavelRepository(conexao)
    repo.salvar(ResponsavelFactory.criar(id=None, cemep_id=cemep_salvo.id, nome="RESPONSAVEL UM"))
    repo.salvar(ResponsavelFactory.criar(id=None, cemep_id=cemep_salvo.id, nome="RESPONSAVEL DOIS"))

    encontrados = repo.buscar_por_cemep(cemep_salvo.id)

    assert len(encontrados) == 2


def test_atualizar_persiste_mudanca(conexao, cemep_salvo):
    repo = SqliteResponsavelRepository(conexao)
    salvo = repo.salvar(ResponsavelFactory.criar(id=None, cemep_id=cemep_salvo.id))

    salvo.nome = Nome("NOME ATUALIZADO")
    repo.atualizar(salvo)

    relido = repo.buscar_por_id(salvo.id)
    assert relido.nome.valor == "NOME ATUALIZADO"


def test_remover_sem_turmas(conexao, cemep_salvo):
    repo = SqliteResponsavelRepository(conexao)
    salvo = repo.salvar(ResponsavelFactory.criar(id=None, cemep_id=cemep_salvo.id))

    repo.remover(salvo.id)

    assert repo.buscar_por_id(salvo.id) is None


def test_remover_bloqueado_por_turma(conexao, cemep_salvo):
    repo_resp = SqliteResponsavelRepository(conexao)
    responsavel = repo_resp.salvar(ResponsavelFactory.criar(id=None, cemep_id=cemep_salvo.id))
    SqliteTurmaCemepRepository(conexao).salvar(
        TurmaCemepFactory.criar(id=None, responsavel_id=responsavel.id)
    )

    with pytest.raises(ResponsavelPossuiTurmasError):
        repo_resp.remover(responsavel.id)
