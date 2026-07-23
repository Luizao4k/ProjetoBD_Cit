"""
Conexão do banco SQLite.

Este módulo é o único lugar do projeto que sabe que o banco é SQLite.
Nenhuma outra camada (domain, application) depende disto.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from shared.exceptions import (
    ConexaoBancoError,
    PersistenciaError,
)

from .schema import SCHEMA


def criar_conexao(
    caminho_banco: str | Path = "escolas.db",
) -> sqlite3.Connection:
    """Cria a conexão com o banco sqlite3"""
    try:
        conexao = sqlite3.connect(
            caminho_banco,
            check_same_thread=False,
        )

        conexao.row_factory = sqlite3.Row
        conexao.execute("PRAGMA foreign_keys = ON")

        return conexao

    except sqlite3.Error as exc:
        raise ConexaoBancoError(
            f"Não foi possível conectar ao banco '{caminho_banco}'."
        ) from exc


def criar_schema(conexao: sqlite3.Connection) -> None:
    try:
        conexao.executescript(SCHEMA)
        conexao.commit()

    except sqlite3.Error as exc:
        conexao.rollback()
        raise PersistenciaError(
            "Falha ao criar o schema."
        ) from exc
