"""
Implementação SQLite do ResponsavelRepository.
"""

from __future__ import annotations

import sqlite3

from domain.entities import Responsavel
from domain.repositories import ResponsavelRepository
from domain.value_objects import Nome
from shared.types import CemepId, ResponsavelId
from shared.exceptions import (
    CemepNaoEncontradoError,
    ResponsavelPossuiTurmasError,
    PersistenciaError,
)

from .._util import parse_datetime, obter_id_gerado


class SqliteResponsavelRepository(ResponsavelRepository):
    """
    Persiste Responsáveis numa tabela SQLite.

    cemep_id não é UNIQUE (relação 1:N) — não há cenário de
    "duplicidade" ao salvar, só a possibilidade do cemep_id informado
    não existir (FOREIGN KEY). Ao remover, um Responsável com Turmas
    CEMEP vinculadas também viola FOREIGN KEY.
    """

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao

#-----------------------------------------------------------------#

    def salvar(self, responsavel: Responsavel) -> Responsavel:
        try:
            cursor = self._conexao.execute(
                """
                INSERT INTO responsaveis (cemep_id, nome, criado_em, atualizado_em)
                VALUES (?, ?, ?, ?)
                """,
                (
                    responsavel.cemep_id,
                    responsavel.nome.valor,
                    responsavel.criado_em.isoformat(),
                    responsavel.atualizado_em.isoformat(),
                ),
            )

            # Não comita mais aqui: quem decide quando confirmar
            # (por linha, por requisição, ...) é o chamador -- ver
            # infrastructure/container/container.py:finalizar() e
            # importacao/pipeline.py.

            responsavel.id = ResponsavelId(obter_id_gerado(cursor))
            return responsavel

        except sqlite3.IntegrityError as exc:
            raise CemepNaoEncontradoError(responsavel.cemep_id) from exc

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao salvar o Responsável.") from exc

#-----------------------------------------------------------------#

    def buscar_por_id(self, responsavel_id: ResponsavelId) -> Responsavel | None:
        try:
            linha = self._conexao.execute(
                "SELECT * FROM responsaveis WHERE id = ?", (responsavel_id,)
            ).fetchone()

            return self._para_entidade(linha) if linha else None

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao buscar o Responsável.") from exc

#-----------------------------------------------------------------#

    def buscar_por_cemep(self, cemep_id: CemepId) -> list[Responsavel]:
        try:
            linhas = self._conexao.execute(
                "SELECT * FROM responsaveis WHERE cemep_id = ? ORDER BY id",
                (cemep_id,),
            ).fetchall()
            return [self._para_entidade(linha) for linha in linhas]

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao buscar os Responsáveis do CEMEP.") from exc

#-----------------------------------------------------------------#

    def listar_todas(self) -> list[Responsavel]:
        try:
            linhas = self._conexao.execute(
                "SELECT * FROM responsaveis ORDER BY id"
            ).fetchall()
            return [self._para_entidade(linha) for linha in linhas]

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao listar os Responsáveis.") from exc

#-----------------------------------------------------------------#

    def atualizar(self, responsavel: Responsavel) -> Responsavel:
        try:
            self._conexao.execute(
                """
                UPDATE responsaveis
                   SET nome = ?, atualizado_em = ?
                 WHERE id = ?
                """,
                (
                    responsavel.nome.valor,
                    responsavel.atualizado_em.isoformat(),
                    responsavel.id,
                ),
            )

            # Não comita mais aqui: quem decide quando confirmar
            # (por linha, por requisição, ...) é o chamador -- ver
            # infrastructure/container/container.py:finalizar() e
            # importacao/pipeline.py.

            return responsavel

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao atualizar o Responsável.") from exc

#-----------------------------------------------------------------#

    def remover(self, responsavel_id: ResponsavelId) -> None:
        try:
            self._conexao.execute(
                "DELETE FROM responsaveis WHERE id = ?", (responsavel_id,)
            )
            # Não comita mais aqui: quem decide quando confirmar
            # (por linha, por requisição, ...) é o chamador -- ver
            # infrastructure/container/container.py:finalizar() e
            # importacao/pipeline.py.

        except sqlite3.IntegrityError as exc:
            raise ResponsavelPossuiTurmasError() from exc

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao remover o Responsável.") from exc

#-----------------------------------------------------------------#

    @staticmethod
    def _para_entidade(linha: sqlite3.Row) -> Responsavel:
        return Responsavel(
            id=ResponsavelId(linha["id"]),
            cemep_id=CemepId(linha["cemep_id"]),
            nome=Nome(linha["nome"]),
            criado_em=parse_datetime(linha["criado_em"]),
            atualizado_em=parse_datetime(linha["atualizado_em"]),
        )
