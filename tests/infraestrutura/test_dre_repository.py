"""
Testes de integração do SqliteDreRepository (banco real em memória).
"""

import pytest

from infrastructure.database.sqlite.repositories import (
    SqliteDreRepository,
    SqliteEscolaRepository,
)
from domain.value_objects import Nome, Telefone
from shared.exceptions import DrePossuiEscolasError
from tests.factories import DreFactory, EscolaFactory


def test_salvar_atribui_id_e_persiste(conexao):
    repo = SqliteDreRepository(conexao)
    dre = DreFactory.criar(id=None)

    salva = repo.salvar(dre)

    assert salva.id is not None
    encontrada = repo.buscar_por_id(salva.id)
    assert encontrada is not None
    assert encontrada.nome == salva.nome
    assert encontrada.telefone == salva.telefone


def test_buscar_por_id_inexistente_retorna_none(conexao):
    repo = SqliteDreRepository(conexao)
    assert repo.buscar_por_id(999999) is None


def test_listar_todas(conexao):
    repo = SqliteDreRepository(conexao)
    repo.salvar(DreFactory.criar(id=None, nome="DRE BELÉM"))
    repo.salvar(DreFactory.criar(id=None, nome="DRE MARABÁ"))

    todas = repo.listar_todas()

    assert len(todas) == 2


def test_atualizar_persiste_mudanca(conexao):
    repo = SqliteDreRepository(conexao)
    salva = repo.salvar(DreFactory.criar(id=None))

    salva.nome = Nome("DRE ATUALIZADA")
    salva.telefone = Telefone("91988887777")
    repo.atualizar(salva)

    relida = repo.buscar_por_id(salva.id)
    assert relida.nome.valor == "DRE ATUALIZADA"
    assert relida.telefone.valor == "91988887777"


def test_remover(conexao):
    repo = SqliteDreRepository(conexao)
    salva = repo.salvar(DreFactory.criar(id=None))

    repo.remover(salva.id)

    assert repo.buscar_por_id(salva.id) is None


def test_remover_dre_com_escola_vinculada_levanta_erro(conexao):
    repo_dre = SqliteDreRepository(conexao)
    repo_escola = SqliteEscolaRepository(conexao)

    dre = repo_dre.salvar(DreFactory.criar(id=None))
    repo_escola.salvar(EscolaFactory.criar(id=None, dre_id=dre.id))

    with pytest.raises(DrePossuiEscolasError):
        repo_dre.remover(dre.id)


def test_buscar_por_nome_encontra(conexao):
    repo = SqliteDreRepository(conexao)
    repo.salvar(DreFactory.criar(id=None, nome="dre belém"))

    encontradas = repo.buscar_por_nome(Nome("dre belém"))

    assert len(encontradas) == 1
    assert encontradas[0].nome.valor == "DRE BELEM"


def test_buscar_por_nome_sem_correspondencia_retorna_lista_vazia(conexao):
    repo = SqliteDreRepository(conexao)
    repo.salvar(DreFactory.criar(id=None, nome="dre belém"))

    assert repo.buscar_por_nome(Nome("dre inexistente")) == []


def test_buscar_por_nome_com_duas_dres_de_mesmo_nome(conexao):
    repo = SqliteDreRepository(conexao)
    repo.salvar(DreFactory.criar(id=None, nome="dre duplicada"))
    repo.salvar(DreFactory.criar(id=None, nome="dre duplicada"))

    assert len(repo.buscar_por_nome(Nome("dre duplicada"))) == 2
