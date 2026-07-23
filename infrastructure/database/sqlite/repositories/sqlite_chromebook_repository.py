"""
Implementação SQLite do ChromebookRepository.
"""

from __future__ import annotations

import sqlite3

from domain.entities import Chromebook
from domain.repositories import ChromebookRepository
from domain.value_objects import Quantidade
from shared.types import ChromebooksId, EscolaId

from .._util import parse_datetime, obter_lastrowid


class SqliteChromebookRepository(ChromebookRepository):
    """
    Persiste registros de Chromebook numa tabela SQLite.

    escola_id é UNIQUE no schema (relação 1:1) — tentar salvar um
    segundo registro para a mesma escola levanta sqlite3.IntegrityError.
    """

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao

    def salvar(self, chromebook: Chromebook) -> Chromebook:
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
        self._conexao.commit()
        chromebook.id = ChromebooksId(obter_lastrowid(cursor))
        return chromebook

    def buscar_por_id(self, chromebook_id: ChromebooksId) -> Chromebook | None:
        linha = self._conexao.execute(
            "SELECT * FROM chromebooks WHERE id = ?", (chromebook_id,)
        ).fetchone()
        return self._para_entidade(linha) if linha else None

    def buscar_por_escola(self, escola_id: EscolaId) -> Chromebook | None:
        linha = self._conexao.execute(
            "SELECT * FROM chromebooks WHERE escola_id = ?", (escola_id,)
        ).fetchone()
        return self._para_entidade(linha) if linha else None

    def listar_todas(self) -> list[Chromebook]:
        linhas = self._conexao.execute(
            "SELECT * FROM chromebooks ORDER BY id"
        ).fetchall()
        return [self._para_entidade(linha) for linha in linhas]

    def atualizar(self, chromebook: Chromebook) -> Chromebook:
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
        self._conexao.commit()
        return chromebook

    def remover(self, chromebook_id: ChromebooksId) -> None:
        self._conexao.execute(
            "DELETE FROM chromebooks WHERE id = ?", (chromebook_id,)
        )
        self._conexao.commit()

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
