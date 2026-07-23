"""
Implementação SQLite do CemepRepository.
"""

from __future__ import annotations

import sqlite3

from domain.entities import Cemep
from domain.repositories import CemepRepository
from shared.types import CemepId, EscolaId
from shared.exceptions import (
    EscolaJaPossuiCemepError,
    CemepPossuiResponsaveisError,
    PersistenciaError,
    )

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

#-----------------------------------------------------------------#

    def salvar(self, cemep: Cemep) -> Cemep:
        try:
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

        except sqlite3.IntegrityError as exc:
            raise EscolaJaPossuiCemepError() from exc

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao salvar o CEMEP.") from exc

#-----------------------------------------------------------------#

    def buscar_por_id(self, cemep_id: CemepId) -> Cemep | None:
        try:
            linha = self._conexao.execute(
                "SELECT * FROM cemeps WHERE id = ?",
                (cemep_id,),
            ).fetchone()

            return self._para_entidade(linha) if linha else None

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError(
                "Falha ao buscar o CEMEP."
            ) from exc

#-----------------------------------------------------------------#

    def buscar_por_escola(self, escola_id: EscolaId) -> Cemep | None:
        try:
            linha = self._conexao.execute(
                "SELECT * FROM cemeps WHERE escola_id = ?", (escola_id,)
            ).fetchone()
            return self._para_entidade(linha) if linha else None

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao buscar o CEMEP da Escola.") from exc

#-----------------------------------------------------------------#

    def listar_todas(self) -> list[Cemep]:

        try:
            linhas = self._conexao.execute("SELECT * FROM cemeps ORDER BY id").fetchall()
            return [self._para_entidade(linha) for linha in linhas]

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao listar os CEMEPs.") from exc

#-----------------------------------------------------------------#

    def atualizar(self, cemep: Cemep) -> Cemep:
        try:
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

            confirmar_transacao(self._conexao)

            return cemep

        except sqlite3.IntegrityError as exc:
            raise EscolaJaPossuiCemepError() from exc

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao atualizar o CEMEP.") from exc

#-----------------------------------------------------------------#

    def remover(self, cemep_id: CemepId) -> None:
        try:
            self._conexao.execute(
                "DELETE FROM cemeps WHERE id = ?",
                (cemep_id,),
            )

            confirmar_transacao(self._conexao)

        except sqlite3.IntegrityError as exc:
            raise CemepPossuiResponsaveisError() from exc

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao remover o CEMEP.") from exc

#-----------------------------------------------------------------#

    @staticmethod
    def _para_entidade(linha: sqlite3.Row) -> Cemep:
        return Cemep(
            id=CemepId(linha["id"]),
            escola_id=EscolaId(linha["escola_id"]),
            comentario=linha["comentario"],
            criado_em=parse_datetime(linha["criado_em"]),
            atualizado_em=parse_datetime(linha["atualizado_em"]),
        )
