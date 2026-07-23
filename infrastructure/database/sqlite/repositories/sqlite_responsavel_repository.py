"""
Implementação SQLite do ResponsavelRepository.
"""

from __future__ import annotations

import sqlite3

from domain.entities import Responsavel
from domain.repositories import ResponsavelRepository
from domain.value_objects import Nome
from shared.types import CemepId, ResponsavelId

from .._util import parse_datetime, obter_lastrowid


class SqliteResponsavelRepository(ResponsavelRepository):
    """
    Persiste Responsáveis numa tabela SQLite.
    """

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao

    def salvar(self, responsavel: Responsavel) -> Responsavel:
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
        self._conexao.commit()
        responsavel.id = ResponsavelId(obter_lastrowid(cursor))
        return responsavel

    def buscar_por_id(self, responsavel_id: ResponsavelId) -> Responsavel | None:
        linha = self._conexao.execute(
            "SELECT * FROM responsaveis WHERE id = ?", (responsavel_id,)
        ).fetchone()
        return self._para_entidade(linha) if linha else None

    def buscar_por_cemep(self, cemep_id: CemepId) -> list[Responsavel]:
        linhas = self._conexao.execute(
            "SELECT * FROM responsaveis WHERE cemep_id = ? ORDER BY id",
            (cemep_id,),
        ).fetchall()
        return [self._para_entidade(linha) for linha in linhas]

    def listar_todas(self) -> list[Responsavel]:
        linhas = self._conexao.execute(
            "SELECT * FROM responsaveis ORDER BY id"
        ).fetchall()
        return [self._para_entidade(linha) for linha in linhas]

    def atualizar(self, responsavel: Responsavel) -> Responsavel:
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
        self._conexao.commit()
        return responsavel

    def remover(self, responsavel_id: ResponsavelId) -> None:
        self._conexao.execute(
            "DELETE FROM responsaveis WHERE id = ?", (responsavel_id,)
        )
        self._conexao.commit()

    @staticmethod
    def _para_entidade(linha: sqlite3.Row) -> Responsavel:
        return Responsavel(
            id=ResponsavelId(linha["id"]),
            cemep_id=CemepId(linha["cemep_id"]),
            nome=Nome(linha["nome"]),
            criado_em=parse_datetime(linha["criado_em"]),
            atualizado_em=parse_datetime(linha["atualizado_em"]),
        )
