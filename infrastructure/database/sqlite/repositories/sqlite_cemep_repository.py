"""
Implementação SQLite do CemepRepository.
"""

from __future__ import annotations

import sqlite3

from domain.entities import Cemep
from domain.repositories import CemepRepository
from shared.types import CemepId, EscolaId

from .._util import parse_datetime, confirmar_transacao, obter_id_gerado


class SqliteCemepRepository(CemepRepository):
    """
    Persiste Cemeps numa tabela SQLite.

    escola_id é UNIQUE no schema (relação 1:1) — tentar salvar um
    segundo Cemep para a mesma escola levanta sqlite3.IntegrityError.

    comentario é gravado como TEXT livre, sem validação (o domínio
    também não valida hoje — ver Comentario VO, ainda não conectado
    à entidade Cemep).
    """

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao

    def salvar(self, cemep: Cemep) -> Cemep:
        cursor = self._conexao.execute(
            """
            INSERT INTO cemeps (escola_id, comentario, criado_em, atualizado_em)
            VALUES (?, ?, ?, ?)
            """,
            (
                cemep.escola_id,
                cemep.comentario,
                cemep.criado_em.isoformat(),
                cemep.atualizado_em.isoformat(),
            ),
        )

        confirmar_transacao(self._conexao)

        cemep.id = CemepId(obter_id_gerado(cursor))
        return cemep

    def buscar_por_id(self, cemep_id: CemepId) -> Cemep | None:
        linha = self._conexao.execute(
            "SELECT * FROM cemeps WHERE id = ?", (cemep_id,)
        ).fetchone()
        return self._para_entidade(linha) if linha else None

    def buscar_por_escola(self, escola_id: EscolaId) -> Cemep | None:
        linha = self._conexao.execute(
            "SELECT * FROM cemeps WHERE escola_id = ?", (escola_id,)
        ).fetchone()
        return self._para_entidade(linha) if linha else None

    def listar_todas(self) -> list[Cemep]:
        linhas = self._conexao.execute("SELECT * FROM cemeps ORDER BY id").fetchall()
        return [self._para_entidade(linha) for linha in linhas]

    def atualizar(self, cemep: Cemep) -> Cemep:
        self._conexao.execute(
            """
            UPDATE cemeps
               SET comentario = ?, atualizado_em = ?
             WHERE id = ?
            """,
            (
                cemep.comentario,
                cemep.atualizado_em.isoformat(),
                cemep.id,
            ),
        )
        self._conexao.commit()
        return cemep

    def remover(self, cemep_id: CemepId) -> None:
        self._conexao.execute("DELETE FROM cemeps WHERE id = ?", (cemep_id,))
        self._conexao.commit()

    @staticmethod
    def _para_entidade(linha: sqlite3.Row) -> Cemep:
        return Cemep(
            id=CemepId(linha["id"]),
            escola_id=EscolaId(linha["escola_id"]),
            comentario=linha["comentario"],
            criado_em=parse_datetime(linha["criado_em"]),
            atualizado_em=parse_datetime(linha["atualizado_em"]),
        )
