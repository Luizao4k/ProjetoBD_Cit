"""
Implementação SQLite do ChromebookRepository.
"""

from __future__ import annotations

import sqlite3

from domain.entities import Chromebook
from domain.repositories import ChromebookRepository
from domain.value_objects import Quantidade
from shared.types import ChromebooksId, EscolaId
from shared.exceptions import (
    EscolaJaPossuiChromebookError,
    EscolaNaoEncontradaError,
    PersistenciaError,
)

from .._util import (
    parse_datetime,
    obter_id_gerado,
    eh_violacao_unique,
    eh_violacao_foreign_key,
)


class SqliteChromebookRepository(ChromebookRepository):
    """
    Persiste registros de Chromebook numa tabela SQLite.

    escola_id é UNIQUE no schema (relação 1:1). Um IntegrityError ao
    salvar significa uma de duas coisas: a escola já tem um registro
    de Chromebook (UNIQUE) ou o escola_id informado não existe
    (FOREIGN KEY) — distinguíveis pelo texto da mensagem do SQLite.

    Nada referencia chromebooks.id como chave estrangeira, então
    `remover` não tem cenário de violação de integridade a tratar.
    """

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao

#-----------------------------------------------------------------#

    def salvar(self, chromebook: Chromebook) -> Chromebook:
        try:
            cursor = self._conexao.execute(
                """
                INSERT INTO chromebooks (escola_id, kit_aluno, kit_professor, criado_em, atualizado_em)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    chromebook.escola_id,
                    int(chromebook.kit_aluno) if chromebook.kit_aluno is not None else None,
                    int(chromebook.kit_professor) if chromebook.kit_professor is not None else None,
                    chromebook.criado_em.isoformat(),
                    chromebook.atualizado_em.isoformat(),
                ),
            )

            # Não comita mais aqui: quem decide quando confirmar
            # (por linha, por requisição, ...) é o chamador -- ver
            # infrastructure/container/container.py:finalizar() e
            # importacao/pipeline.py.

            chromebook.id = ChromebooksId(obter_id_gerado(cursor))
            return chromebook

        except sqlite3.IntegrityError as exc:
            if eh_violacao_unique(exc):
                raise EscolaJaPossuiChromebookError() from exc
            if eh_violacao_foreign_key(exc):
                raise EscolaNaoEncontradaError(chromebook.escola_id) from exc
            raise PersistenciaError("Falha de integridade ao salvar o Chromebook.") from exc

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao salvar o Chromebook.") from exc

#-----------------------------------------------------------------#

    def buscar_por_id(self, chromebook_id: ChromebooksId) -> Chromebook | None:
        try:
            linha = self._conexao.execute(
                "SELECT * FROM chromebooks WHERE id = ?", (chromebook_id,)
            ).fetchone()

            return self._para_entidade(linha) if linha else None

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao buscar o Chromebook.") from exc

#-----------------------------------------------------------------#

    def buscar_por_escola(self, escola_id: EscolaId) -> Chromebook | None:
        try:
            linha = self._conexao.execute(
                "SELECT * FROM chromebooks WHERE escola_id = ?", (escola_id,)
            ).fetchone()

            return self._para_entidade(linha) if linha else None

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao buscar o Chromebook da Escola.") from exc

#-----------------------------------------------------------------#

    def listar_todas(self) -> list[Chromebook]:
        try:
            linhas = self._conexao.execute(
                "SELECT * FROM chromebooks ORDER BY id"
            ).fetchall()
            return [self._para_entidade(linha) for linha in linhas]

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao listar os Chromebooks.") from exc

#-----------------------------------------------------------------#

    def atualizar(self, chromebook: Chromebook) -> Chromebook:
        try:
            self._conexao.execute(
                """
                UPDATE chromebooks
                   SET kit_aluno = ?, kit_professor = ?, atualizado_em = ?
                 WHERE id = ?
                """,
                (
                    int(chromebook.kit_aluno) if chromebook.kit_aluno is not None else None,
                    int(chromebook.kit_professor) if chromebook.kit_professor is not None else None,
                    chromebook.atualizado_em.isoformat(),
                    chromebook.id,
                ),
            )

            # Não comita mais aqui: quem decide quando confirmar
            # (por linha, por requisição, ...) é o chamador -- ver
            # infrastructure/container/container.py:finalizar() e
            # importacao/pipeline.py.

            return chromebook

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao atualizar o Chromebook.") from exc

#-----------------------------------------------------------------#

    def remover(self, chromebook_id: ChromebooksId) -> None:
        try:
            self._conexao.execute(
                "DELETE FROM chromebooks WHERE id = ?", (chromebook_id,)
            )
            # Não comita mais aqui: quem decide quando confirmar
            # (por linha, por requisição, ...) é o chamador -- ver
            # infrastructure/container/container.py:finalizar() e
            # importacao/pipeline.py.

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao remover o Chromebook.") from exc

#-----------------------------------------------------------------#

    @staticmethod
    def _para_entidade(linha: sqlite3.Row) -> Chromebook:
        return Chromebook(
            id=ChromebooksId(linha["id"]),
            escola_id=EscolaId(linha["escola_id"]),
            kit_aluno=(
                Quantidade(linha["kit_aluno"])
                if linha["kit_aluno"] is not None
                else None
            ),
            kit_professor=(
                Quantidade(linha["kit_professor"])
                if linha["kit_professor"] is not None
                else None
            ),
            criado_em=parse_datetime(linha["criado_em"]),
            atualizado_em=parse_datetime(linha["atualizado_em"]),
        )
