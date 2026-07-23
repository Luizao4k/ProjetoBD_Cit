"""
Implementação SQLite do DiretorRepository.
"""

from __future__ import annotations

import sqlite3

from domain.entities import Diretor
from domain.repositories import DiretorRepository
from domain.value_objects import Email, Nome, Telefone
from shared.types import DiretorId, EscolaId

from .._util import parse_datetime, obter_lastrowid


class SqliteDiretorRepository(DiretorRepository):
    """
    Persiste Diretores numa tabela SQLite.

    escola_id é UNIQUE no schema (relação 1:1) — tentar salvar um
    segundo Diretor para a mesma escola levanta sqlite3.IntegrityError.
    """

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao

    def salvar(self, diretor: Diretor) -> Diretor:
        cursor = self._conexao.execute(
            """
            INSERT INTO diretores (escola_id, nome, telefone, email, criado_em, atualizado_em)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                diretor.escola_id,
                diretor.nome.valor,
                diretor.telefone.valor if diretor.telefone else None,
                diretor.email.valor if diretor.email else None,
                diretor.criado_em.isoformat(),
                diretor.atualizado_em.isoformat(),
            ),
        )
        self._conexao.commit()
        diretor.id = DiretorId(obter_lastrowid(cursor))
        return diretor

    def buscar_por_id(self, diretor_id: DiretorId) -> Diretor | None:
        linha = self._conexao.execute(
            "SELECT * FROM diretores WHERE id = ?", (diretor_id,)
        ).fetchone()
        return self._para_entidade(linha) if linha else None

    def buscar_por_escola(self, escola_id: EscolaId) -> Diretor | None:
        linha = self._conexao.execute(
            "SELECT * FROM diretores WHERE escola_id = ?", (escola_id,)
        ).fetchone()
        return self._para_entidade(linha) if linha else None

    def listar_todas(self) -> list[Diretor]:
        linhas = self._conexao.execute(
            "SELECT * FROM diretores ORDER BY id"
        ).fetchall()
        return [self._para_entidade(linha) for linha in linhas]

    def atualizar(self, diretor: Diretor) -> Diretor:
        self._conexao.execute(
            """
            UPDATE diretores
               SET nome = ?, telefone = ?, email = ?, atualizado_em = ?
             WHERE id = ?
            """,
            (
                diretor.nome.valor,
                diretor.telefone.valor if diretor.telefone else None,
                diretor.email.valor if diretor.email else None,
                diretor.atualizado_em.isoformat(),
                diretor.id,
            ),
        )
        self._conexao.commit()
        return diretor

    def remover(self, diretor_id: DiretorId) -> None:
        self._conexao.execute("DELETE FROM diretores WHERE id = ?", (diretor_id,))
        self._conexao.commit()

    @staticmethod
    def _para_entidade(linha: sqlite3.Row) -> Diretor:
        return Diretor(
            id=DiretorId(linha["id"]),
            escola_id=EscolaId(linha["escola_id"]),
            nome=Nome(linha["nome"]),
            telefone=Telefone(linha["telefone"]) if linha["telefone"] else None,
            email=Email(linha["email"]) if linha["email"] else None,
            criado_em=parse_datetime(linha["criado_em"]),
            atualizado_em=parse_datetime(linha["atualizado_em"]),
        )
