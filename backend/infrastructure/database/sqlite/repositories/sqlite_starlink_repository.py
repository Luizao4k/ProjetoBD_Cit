"""
Implementação SQLite do StarlinkRepository.
"""

from __future__ import annotations

import sqlite3

from domain.entities import Starlink
from domain.repositories import StarlinkRepository
from domain.value_objects import Nome
from shared.types import EscolaId, StarlinkId
from shared.exceptions import (
    EscolaNaoEncontradaError,
    PersistenciaError,
)

from .._util import parse_datetime, obter_id_gerado


class SqliteStarlinkRepository(StarlinkRepository):
    """
    Persiste designações de Starlink numa tabela SQLite.

    Diferente de Diretor/Cemep/Chromebook, escola_id NÃO é UNIQUE aqui
    — uma escola pode ter mais de uma designação (relação 1:N), então
    não há cenário de "duplicidade" ao salvar, só a possibilidade do
    escola_id informado não existir (FOREIGN KEY).

    Nada referencia starlinks.id como chave estrangeira, então
    `remover` não tem cenário de violação de integridade a tratar.
    """

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao

#-----------------------------------------------------------------#

    def salvar(self, starlink: Starlink) -> Starlink:
        try:
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

            # Não comita mais aqui: quem decide quando confirmar
            # (por linha, por requisição, ...) é o chamador -- ver
            # infrastructure/container/container.py:finalizar() e
            # importacao/pipeline.py.

            starlink.id = StarlinkId(obter_id_gerado(cursor))
            return starlink

        except sqlite3.IntegrityError as exc:
            raise EscolaNaoEncontradaError(starlink.escola_id) from exc

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao salvar o Starlink.") from exc

#-----------------------------------------------------------------#

    def buscar_por_id(self, starlink_id: StarlinkId) -> Starlink | None:
        try:
            linha = self._conexao.execute(
                "SELECT * FROM starlinks WHERE id = ?", (starlink_id,)
            ).fetchone()

            return self._para_entidade(linha) if linha else None

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao buscar o Starlink.") from exc

#-----------------------------------------------------------------#

    def buscar_por_escola(self, escola_id: EscolaId) -> list[Starlink]:
        try:
            linhas = self._conexao.execute(
                "SELECT * FROM starlinks WHERE escola_id = ? ORDER BY id",
                (escola_id,),
            ).fetchall()
            return [self._para_entidade(linha) for linha in linhas]

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao buscar os Starlinks da Escola.") from exc

#-----------------------------------------------------------------#

    def buscar_por_designacao(self, designacao: str) -> Starlink | None:
        try:
            linha = self._conexao.execute(
                """
                SELECT *
                FROM starlinks
                WHERE designacao = ?
                """,
                (designacao,),
            ).fetchone()

            return self._para_entidade(linha) if linha else None

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError(
                "Falha ao buscar Starlink pela designação."
            ) from exc

#-----------------------------------------------------------------#

    def listar_todas(self) -> list[Starlink]:
        try:
            linhas = self._conexao.execute(
                "SELECT * FROM starlinks ORDER BY id"
            ).fetchall()
            return [self._para_entidade(linha) for linha in linhas]

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao listar os Starlinks.") from exc

#-----------------------------------------------------------------#

    def atualizar(self, starlink: Starlink) -> Starlink:
        try:
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

            # Não comita mais aqui: quem decide quando confirmar
            # (por linha, por requisição, ...) é o chamador -- ver
            # infrastructure/container/container.py:finalizar() e
            # importacao/pipeline.py.

            return starlink

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao atualizar o Starlink.") from exc

#-----------------------------------------------------------------#

    def remover(self, starlink_id: StarlinkId) -> None:
        try:
            self._conexao.execute("DELETE FROM starlinks WHERE id = ?", (starlink_id,))
            # Não comita mais aqui: quem decide quando confirmar
            # (por linha, por requisição, ...) é o chamador -- ver
            # infrastructure/container/container.py:finalizar() e
            # importacao/pipeline.py.

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao remover o Starlink.") from exc

#-----------------------------------------------------------------#

    @staticmethod
    def _para_entidade(linha: sqlite3.Row) -> Starlink:
        return Starlink(
            id=StarlinkId(linha["id"]),
            escola_id=EscolaId(linha["escola_id"]),
            designacao=Nome(linha["designacao"]),
            criado_em=parse_datetime(linha["criado_em"]),
            atualizado_em=parse_datetime(linha["atualizado_em"]),
        )
