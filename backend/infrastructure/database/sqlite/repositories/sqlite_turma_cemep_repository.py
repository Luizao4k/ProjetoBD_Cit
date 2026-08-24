"""
Implementação SQLite do TurmaCemepRepository.
"""

from __future__ import annotations

import sqlite3

from domain.entities import TurmaCemep
from domain.repositories import TurmaCemepRepository
from domain.value_objects import Nome
from shared.types import ResponsavelId, TurmaCemepId
from shared.exceptions import (
    ResponsavelNaoEncontradoError,
    PersistenciaError,
)

from .._util import parse_datetime, obter_id_gerado


class SqliteTurmaCemepRepository(TurmaCemepRepository):
    """
    Persiste Turmas do Cemep numa tabela SQLite.

    responsavel_id não é UNIQUE (relação 1:N) — não há cenário de
    "duplicidade" ao salvar, só a possibilidade do responsavel_id
    informado não existir (FOREIGN KEY).

    Nada referencia turmas_cemep.id como chave estrangeira, então
    `remover` não tem cenário de violação de integridade a tratar.
    """

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao

#-----------------------------------------------------------------#

    def salvar(self, turma: TurmaCemep) -> TurmaCemep:
        try:
            cursor = self._conexao.execute(
                """
                INSERT INTO turmas_cemep (responsavel_id, nome_turma, criado_em, atualizado_em)
                VALUES (?, ?, ?, ?)
                """,
                (
                    turma.responsavel_id,
                    turma.nome_turma.valor,
                    turma.criado_em.isoformat(),
                    turma.atualizado_em.isoformat(),
                ),
            )

            # Não comita mais aqui: quem decide quando confirmar
            # (por linha, por requisição, ...) é o chamador -- ver
            # infrastructure/container/container.py:finalizar() e
            # importacao/pipeline.py.

            turma.id = TurmaCemepId(obter_id_gerado(cursor))
            return turma

        except sqlite3.IntegrityError as exc:
            raise ResponsavelNaoEncontradoError(turma.responsavel_id) from exc

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao salvar a Turma CEMEP.") from exc

#-----------------------------------------------------------------#

    def buscar_por_id(self, turma_id: TurmaCemepId) -> TurmaCemep | None:
        try:
            linha = self._conexao.execute(
                "SELECT * FROM turmas_cemep WHERE id = ?", (turma_id,)
            ).fetchone()

            return self._para_entidade(linha) if linha else None

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao buscar a Turma CEMEP.") from exc

#-----------------------------------------------------------------#

    def buscar_por_responsavel(
        self, responsavel_id: ResponsavelId
    ) -> list[TurmaCemep]:
        try:
            linhas = self._conexao.execute(
                "SELECT * FROM turmas_cemep WHERE responsavel_id = ? ORDER BY id",
                (responsavel_id,),
            ).fetchall()
            return [self._para_entidade(linha) for linha in linhas]

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao buscar Turmas do Responsável.") from exc

#-----------------------------------------------------------------#

    def listar_todas(self) -> list[TurmaCemep]:
        try:
            linhas = self._conexao.execute(
                "SELECT * FROM turmas_cemep ORDER BY id"
            ).fetchall()
            return [self._para_entidade(linha) for linha in linhas]

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao listar as Turmas CEMEP.") from exc

#-----------------------------------------------------------------#

    def atualizar(self, turma: TurmaCemep) -> TurmaCemep:
        try:
            self._conexao.execute(
                """
                UPDATE turmas_cemep
                   SET nome_turma = ?, atualizado_em = ?
                 WHERE id = ?
                """,
                (
                    turma.nome_turma.valor,
                    turma.atualizado_em.isoformat(),
                    turma.id,
                ),
            )

            # Não comita mais aqui: quem decide quando confirmar
            # (por linha, por requisição, ...) é o chamador -- ver
            # infrastructure/container/container.py:finalizar() e
            # importacao/pipeline.py.

            return turma

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao atualizar a Turma CEMEP.") from exc

#-----------------------------------------------------------------#

    def remover(self, turma_id: TurmaCemepId) -> None:
        try:
            self._conexao.execute(
                "DELETE FROM turmas_cemep WHERE id = ?", (turma_id,)
            )
            # Não comita mais aqui: quem decide quando confirmar
            # (por linha, por requisição, ...) é o chamador -- ver
            # infrastructure/container/container.py:finalizar() e
            # importacao/pipeline.py.

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao remover a Turma CEMEP.") from exc

#-----------------------------------------------------------------#

    @staticmethod
    def _para_entidade(linha: sqlite3.Row) -> TurmaCemep:
        return TurmaCemep(
            id=TurmaCemepId(linha["id"]),
            responsavel_id=ResponsavelId(linha["responsavel_id"]),
            nome_turma=Nome(linha["nome_turma"]),
            criado_em=parse_datetime(linha["criado_em"]),
            atualizado_em=parse_datetime(linha["atualizado_em"]),
        )
