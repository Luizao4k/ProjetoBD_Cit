"""
Utilitários internos da implementação SQLite.

Este módulo encapsula detalhes específicos do SQLite para evitar que
eles se espalhem pelos repositórios.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime

from shared.exceptions import (
    FalhaAoObterIdGeradoError,
    TransacaoError,
)


def parse_datetime(valor: str) -> datetime:
    """
    Converte uma string ISO 8601 armazenada no banco para um objeto
    ``datetime``.

    É o inverso de ``datetime.isoformat()``, utilizado durante a
    persistência das entidades.
    """
    return datetime.fromisoformat(valor)


def obter_id_gerado(cursor: sqlite3.Cursor) -> int:
    """
    Retorna o identificador gerado pelo último INSERT.

    Raises:
        FalhaAoObterIdGeradoError:
            Caso o SQLite não retorne um identificador.
    """
    lastrowid = cursor.lastrowid

    if lastrowid is None:
        raise FalhaAoObterIdGeradoError(
            "O banco de dados não retornou o identificador gerado."
        )

    return lastrowid


def confirmar_transacao(conexao: sqlite3.Connection) -> None:
    """
    Confirma a transação atual.

    Em caso de falha, desfaz a transação e traduz a exceção do SQLite
    para uma exceção da infraestrutura.
    """
    try:
        conexao.commit()

    except sqlite3.Error as exc:
        conexao.rollback()
        raise TransacaoError(
            "Falha ao confirmar a transação."
        ) from exc
