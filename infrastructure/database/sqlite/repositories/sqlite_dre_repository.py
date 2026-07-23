"""
Implementação SQLite do DreRepository.
"""

from __future__ import annotations

import sqlite3

from domain.entities import Dre
from domain.repositories import DreRepository
from domain.value_objects import Nome, Telefone
from shared.types import DreId

from .._util import parse_datetime, obter_lastrowid


class SqliteDreRepository(DreRepository):
    """
    Persiste DREs numa tabela SQLite.
    """

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao

    def salvar(self, dre: Dre) -> Dre:
        cursor = self._conexao.execute(
            """
            INSERT INTO dres (nome, telefone, criado_em, atualizado_em)
            VALUES (?, ?, ?, ?)
            """,
            (
                dre.nome.valor,
                dre.telefone.valor if dre.telefone else None,
                dre.criado_em.isoformat(),
                dre.atualizado_em.isoformat(),
            ),
        )
        self._conexao.commit()
        dre.id = DreId(obter_lastrowid(cursor))
        return dre

    def buscar_por_id(self, dre_id: DreId) -> Dre | None:
        linha = self._conexao.execute(
            "SELECT * FROM dres WHERE id = ?", (dre_id,)
        ).fetchone()
        return self._para_entidade(linha) if linha else None

    def listar_todas(self) -> list[Dre]:
        linhas = self._conexao.execute("SELECT * FROM dres ORDER BY id").fetchall()
        return [self._para_entidade(linha) for linha in linhas]

    def atualizar(self, dre: Dre) -> Dre:
        self._conexao.execute(
            """
            UPDATE dres
               SET nome = ?, telefone = ?, atualizado_em = ?
             WHERE id = ?
            """,
            (
                dre.nome.valor,
                dre.telefone.valor if dre.telefone else None,
                dre.atualizado_em.isoformat(),
                dre.id,
            ),
        )
        self._conexao.commit()
        return dre

    def remover(self, dre_id: DreId) -> None:
        self._conexao.execute("DELETE FROM dres WHERE id = ?", (dre_id,))
        self._conexao.commit()

    @staticmethod
    def _para_entidade(linha: sqlite3.Row) -> Dre:
        return Dre(
            id=DreId(linha["id"]),
            nome=Nome(linha["nome"]),
            telefone=Telefone(linha["telefone"]) if linha["telefone"] else None,
            criado_em=parse_datetime(linha["criado_em"]),
            atualizado_em=parse_datetime(linha["atualizado_em"]),
        )
