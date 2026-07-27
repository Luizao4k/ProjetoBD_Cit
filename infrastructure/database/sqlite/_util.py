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


def eh_violacao_unique(exc: sqlite3.IntegrityError) -> bool:
    """
    True se o IntegrityError veio de uma constraint UNIQUE.

    A mensagem do SQLite nomeia a tabela e a coluna nesse caso
    (ex: "UNIQUE constraint failed: diretores.escola_id"), o que
    distingue de forma confiável de uma violação de FOREIGN KEY.
    """
    return "Falha na restrição UNIQUE" in str(exc)


def eh_violacao_foreign_key(exc: sqlite3.IntegrityError) -> bool:
    """
    True se o IntegrityError veio de uma constraint FOREIGN KEY.

    Atenção: o SQLite usa a mesma mensagem genérica ("FOREIGN KEY
    constraint failed") tanto para um INSERT/UPDATE que referencia um
    id inexistente quanto para um DELETE bloqueado por um filho — a
    mensagem sozinha não diz qual dos dois. Quem chama esta função
    precisa saber, pelo contexto (qual operação estava em andamento),
    qual dos dois significados se aplica.
    """
    return "Falha na restrição de FOREIGN KEY" in str(exc)


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
