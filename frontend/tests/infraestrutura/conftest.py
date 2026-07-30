"""
Fixtures compartilhadas pelos testes de repositório SQLite.

Cada teste recebe um banco em memória novo, com o schema já criado,
isolado dos demais testes e descartado ao final.
"""

import pytest

from infrastructure.database import criar_conexao, criar_schema


@pytest.fixture
def conexao():
    conn = criar_conexao(":memory:")
    criar_schema(conn)
    yield conn
    conn.close()
