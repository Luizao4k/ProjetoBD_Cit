"""
Implementação SQLite do DreRepository.
"""

from __future__ import annotations

import sqlite3

from domain.entities import Dre
from domain.repositories import DreRepository
from domain.value_objects import Nome, Telefone
from shared.types import DreId
from shared.exceptions import (
    DrePossuiEscolasError,
    PersistenciaError,
)

from .._util import parse_datetime, obter_id_gerado


class SqliteDreRepository(DreRepository):
    """
    Persiste DREs numa tabela SQLite.

    DRE não tem nenhuma constraint UNIQUE além do id — a única
    violação de integridade plausível é ao remover uma DRE que ainda
    possui Escolas vinculadas (FOREIGN KEY em escolas.dre_id).
    """

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao

#-----------------------------------------------------------------#

    def salvar(self, dre: Dre) -> Dre:
        try:
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

            # Não comita mais aqui: quem decide quando confirmar
            # (por linha, por requisição, ...) é o chamador -- ver
            # infrastructure/container/container.py:finalizar() e
            # importacao/pipeline.py.

            dre.id = DreId(obter_id_gerado(cursor))
            return dre

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao salvar a DRE.") from exc

#-----------------------------------------------------------------#

    def buscar_por_id(self, dre_id: DreId) -> Dre | None:
        try:
            linha = self._conexao.execute(
                "SELECT * FROM dres WHERE id = ?", (dre_id,)
            ).fetchone()

            return self._para_entidade(linha) if linha else None

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao buscar a DRE.") from exc

#-----------------------------------------------------------------#

    def buscar_por_nome(self, nome: Nome) -> list[Dre]:
        try:
            linhas = self._conexao.execute(
                "SELECT * FROM dres WHERE nome = ? ORDER BY id", (nome.valor,)
            ).fetchall()
            return [self._para_entidade(linha) for linha in linhas]

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao buscar DREs por nome.") from exc

#-----------------------------------------------------------------#

    def listar_todas(self) -> list[Dre]:
        try:
            linhas = self._conexao.execute("SELECT * FROM dres ORDER BY id").fetchall()
            return [self._para_entidade(linha) for linha in linhas]

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao listar as DREs.") from exc

#-----------------------------------------------------------------#

    def atualizar(self, dre: Dre) -> Dre:
        try:
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

            # Não comita mais aqui: quem decide quando confirmar
            # (por linha, por requisição, ...) é o chamador -- ver
            # infrastructure/container/container.py:finalizar() e
            # importacao/pipeline.py.

            return dre

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao atualizar a DRE.") from exc

#-----------------------------------------------------------------#

    def remover(self, dre_id: DreId) -> None:
        try:
            self._conexao.execute("DELETE FROM dres WHERE id = ?", (dre_id,))
            # Não comita mais aqui: quem decide quando confirmar
            # (por linha, por requisição, ...) é o chamador -- ver
            # infrastructure/container/container.py:finalizar() e
            # importacao/pipeline.py.

        except sqlite3.IntegrityError as exc:
            raise DrePossuiEscolasError() from exc

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao remover a DRE.") from exc

#-----------------------------------------------------------------#

    @staticmethod
    def _para_entidade(linha: sqlite3.Row) -> Dre:
        return Dre(
            id=DreId(linha["id"]),
            nome=Nome(linha["nome"]),
            telefone=Telefone(linha["telefone"]) if linha["telefone"] else None,
            criado_em=parse_datetime(linha["criado_em"]),
            atualizado_em=parse_datetime(linha["atualizado_em"]),
        )
