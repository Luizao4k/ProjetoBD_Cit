"""
Testes de Container.finalizar — o hook de ciclo de vida usado pela
API (um Container por requisição HTTP, ver interface/app.py).
"""

import sqlite3

import pytest

from domain.entities import Dre
from domain.value_objects import Nome
from infrastructure.container.container import Container
from infrastructure.database.sqlite.repositories import SqliteDreRepository


@pytest.fixture
def caminho_banco(tmp_path):
    return str(tmp_path / "teste.db")


def test_finalizar_com_sucesso_confirma_e_fecha(caminho_banco):
    container = Container(caminho_banco)
    # INSERT direto na conexão em vez de via repositório -- mais
    # simples pra este teste, e continua funcionando porque os
    # repositórios não fazem mais nada de especial no INSERT em si,
    # só param de comitar sozinhos (ver test_finalizar_com_sucesso_
    # confirma_escrita_feita_via_repositorio abaixo para a versão via
    # repositório real).
    container._conexao.execute(
        "INSERT INTO dres (nome, criado_em, atualizado_em) "
        "VALUES ('DRE Teste', '2026-01-01T00:00:00', '2026-01-01T00:00:00')"
    )

    container.finalizar(sucesso=True)

    # conexão separada, prova que persistiu de verdade no arquivo
    verificacao = sqlite3.connect(caminho_banco)
    total = verificacao.execute("SELECT COUNT(*) FROM dres").fetchone()[0]
    verificacao.close()
    assert total == 1

    with pytest.raises(sqlite3.ProgrammingError):
        container._conexao.execute("SELECT 1")


def test_finalizar_sem_sucesso_desfaz_e_fecha(caminho_banco):
    container = Container(caminho_banco)
    container._conexao.execute(
        "INSERT INTO dres (nome, criado_em, atualizado_em) "
        "VALUES ('DRE Teste', '2026-01-01T00:00:00', '2026-01-01T00:00:00')"
    )

    container.finalizar(sucesso=False)

    verificacao = sqlite3.connect(caminho_banco)
    total = verificacao.execute("SELECT COUNT(*) FROM dres").fetchone()[0]
    verificacao.close()
    assert total == 0

    with pytest.raises(sqlite3.ProgrammingError):
        container._conexao.execute("SELECT 1")


def test_finalizar_sem_sucesso_desfaz_escrita_feita_via_repositorio_real(caminho_banco):
    """
    O cenário que só passou a ser possível depois do refactor: antes,
    SqliteDreRepository.salvar() comitava sozinho, então não havia
    nada pra este teste desfazer. Hoje, uma escrita feita através de
    um repositório de verdade só se torna permanente quando
    Container.finalizar(sucesso=True) roda -- exatamente o que dá à
    API uma requisição como unidade de transação real.
    """
    container = Container(caminho_banco)
    repo = SqliteDreRepository(container._conexao)

    repo.salvar(Dre(id=None, nome=Nome("DRE Teste"), telefone=None))

    container.finalizar(sucesso=False)

    verificacao = sqlite3.connect(caminho_banco)
    total = verificacao.execute("SELECT COUNT(*) FROM dres").fetchone()[0]
    verificacao.close()
    assert total == 0
