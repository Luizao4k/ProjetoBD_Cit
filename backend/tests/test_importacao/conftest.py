"""
Fixtures compartilhadas pelos testes do pacote importacao.

Uma conexão real em memória por teste (não mock) — mesma filosofia já
usada em tests/infraestrutura/conftest.py: os Mappers fazem consultas
de verdade contra o repositório (buscar_por_inep, buscar_por_escola),
então testar com dublê de repositório escalaria mal e desviaria do
comportamento real.
"""

from __future__ import annotations

import pytest

from domain.entities import Cemep, Dre, Escola
from domain.enums import TipoEscola
from domain.value_objects import Inep, Municipio, Nome
from infrastructure.database import criar_conexao, criar_schema
from infrastructure.database.sqlite.repositories import (
    SqliteCemepRepository,
    SqliteDreRepository,
    SqliteEscolaRepository,
)


@pytest.fixture
def conexao():
    conn = criar_conexao(":memory:")
    criar_schema(conn)
    yield conn
    conn.close()


@pytest.fixture
def repo_dre(conexao):
    return SqliteDreRepository(conexao)


@pytest.fixture
def repo_escola(conexao):
    return SqliteEscolaRepository(conexao)


@pytest.fixture
def repo_cemep(conexao):
    return SqliteCemepRepository(conexao)


@pytest.fixture
def dre_salva(repo_dre):
    return repo_dre.salvar(Dre(id=None, nome=Nome("DRE Belém"), telefone=None))


@pytest.fixture
def escola_salva(repo_escola, dre_salva):
    return repo_escola.salvar(
        Escola(
            id=None,
            inep=Inep("12345678"),
            nome=Nome("Escola Teste"),
            tipo=TipoEscola.MUNICIPAL,
            municipio=Municipio("Belém"),
            dre_id=dre_salva.id,
            endereco=None,
        )
    )


@pytest.fixture
def cemep_salvo(repo_cemep, escola_salva):
    return repo_cemep.salvar(
        Cemep(id=None, escola_id=escola_salva.id, comentario=None)
    )
