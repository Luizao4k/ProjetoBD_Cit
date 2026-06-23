"""
Gerenciamento de conexão SQLite e criação do schema.

Decisões técnicas:
  - WAL mode  → melhor concorrência de leitura.
  - Foreign keys ON  → integridade referencial garantida pelo banco.
  - Row factory = Row  → acesso por nome de coluna.
  - CHECK constraints refletem as regras do domain/value_objects.
"""
from .conexao import (
    criar_conexao_db,
    get_db,
    close_connection,
    init_app,
)

from .schema import inicializar_schema

__all__ = [
    "criar_conexao_db",
    "get_db",
    "close_connection",
    "init_app",
    "inicializar_schema",
]
