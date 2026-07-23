"""
Implementação SQLite do StarlinkRepository.
"""

from __future__ import annotations

import sqlite3

from domain.entities import Starlink
from domain.repositories import StarlinkRepository
from domain.value_objects import Nome
from shared.types import EscolaId, StarlinkId

from .._util import parse_datetime, obter_lastrowid


class SqliteStarlinkRepository(StarlinkRepository):
    """
    Persiste designações de Starlink numa tabela SQLite.

    Diferente de Diretor/Cemep/Chromebook, escola_id NÃO é UNIQUE aqui
    — uma escola pode ter mais de uma designação (relação 1:N).
    """

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao

    def salvar(self, starlink: Starlink) -> Starlink:
        cursor = self._conexao.execute(
            """
            INSERT INTO starlinks (escola_id, designacao, criado_em, atualizado_em)
            VALUES (?, ?, ?, ?)
            """,
            (
                starlink.escola_id,
                starlink.designacao.valor,
                starlink.criado_em.isoformat(),
                starlink.atualizado_em.isoformat(),
            ),
        )
        self._conexao.commit()
        starlink.id = StarlinkId(obter_lastrowid(cursor))
        return starlink

    def buscar_por_id(self, starlink_id: StarlinkId) -> Starlink | None:
        linha = self._conexao.execute(
            "SELECT * FROM starlinks WHERE id = ?", (starlink_id,)
        ).fetchone()
        return self._para_entidade(linha) if linha else None

    def buscar_por_escola(self, escola_id: EscolaId) -> list[Starlink]:
        linhas = self._conexao.execute(
            "SELECT * FROM starlinks WHERE escola_id = ? ORDER BY id",
            (escola_id,),
        ).fetchall()
        return [self._para_entidade(linha) for linha in linhas]

    def listar_todas(self) -> list[Starlink]:
        linhas = self._conexao.execute(
            "SELECT * FROM starlinks ORDER BY id"
        ).fetchall()
        return [self._para_entidade(linha) for linha in linhas]

    def atualizar(self, starlink: Starlink) -> Starlink:
        self._conexao.execute(
            """
            UPDATE starlinks
               SET designacao = ?, atualizado_em = ?
             WHERE id = ?
            """,
            (
                starlink.designacao.valor,
                starlink.atualizado_em.isoformat(),
                starlink.id,
            ),
        )
        self._conexao.commit()
        return starlink

    def remover(self, starlink_id: StarlinkId) -> None:
        self._conexao.execute("DELETE FROM starlinks WHERE id = ?", (starlink_id,))
        self._conexao.commit()

    @staticmethod
    def _para_entidade(linha: sqlite3.Row) -> Starlink:
        return Starlink(
            id=StarlinkId(linha["id"]),
            escola_id=EscolaId(linha["escola_id"]),
            designacao=Nome(linha["designacao"]),
            criado_em=parse_datetime(linha["criado_em"]),
            atualizado_em=parse_datetime(linha["atualizado_em"]),
        )
