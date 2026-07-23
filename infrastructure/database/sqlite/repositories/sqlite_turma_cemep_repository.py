"""
Implementação SQLite do TurmaCemepRepository.
"""

from __future__ import annotations

import sqlite3

from domain.entities import TurmaCemep
from domain.repositories import TurmaCemepRepository
from domain.value_objects import Nome
from shared.types import ResponsavelId, TurmaCemepId

from .._util import parse_datetime, obter_lastrowid


class SqliteTurmaCemepRepository(TurmaCemepRepository):
    """
    Persiste Turmas do Cemep numa tabela SQLite.
    """

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao

    def salvar(self, turma: TurmaCemep) -> TurmaCemep:
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
        self._conexao.commit()
        turma.id = TurmaCemepId(obter_lastrowid(cursor))
        return turma

    def buscar_por_id(self, turma_id: TurmaCemepId) -> TurmaCemep | None:
        linha = self._conexao.execute(
            "SELECT * FROM turmas_cemep WHERE id = ?", (turma_id,)
        ).fetchone()
        return self._para_entidade(linha) if linha else None

    def buscar_por_responsavel(
        self, responsavel_id: ResponsavelId
    ) -> list[TurmaCemep]:
        linhas = self._conexao.execute(
            "SELECT * FROM turmas_cemep WHERE responsavel_id = ? ORDER BY id",
            (responsavel_id,),
        ).fetchall()
        return [self._para_entidade(linha) for linha in linhas]

    def listar_todas(self) -> list[TurmaCemep]:
        linhas = self._conexao.execute(
            "SELECT * FROM turmas_cemep ORDER BY id"
        ).fetchall()
        return [self._para_entidade(linha) for linha in linhas]

    def atualizar(self, turma: TurmaCemep) -> TurmaCemep:
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
        self._conexao.commit()
        return turma

    def remover(self, turma_id: TurmaCemepId) -> None:
        self._conexao.execute(
            "DELETE FROM turmas_cemep WHERE id = ?", (turma_id,)
        )
        self._conexao.commit()

    @staticmethod
    def _para_entidade(linha: sqlite3.Row) -> TurmaCemep:
        return TurmaCemep(
            id=TurmaCemepId(linha["id"]),
            responsavel_id=ResponsavelId(linha["responsavel_id"]),
            nome_turma=Nome(linha["nome_turma"]),
            criado_em=parse_datetime(linha["criado_em"]),
            atualizado_em=parse_datetime(linha["atualizado_em"]),
        )
