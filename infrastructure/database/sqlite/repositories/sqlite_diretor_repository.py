"""
Implementação SQLite do DiretorRepository.
"""

from __future__ import annotations

import sqlite3

from domain.entities import Diretor
from domain.repositories import DiretorRepository
from domain.value_objects import Email, Nome, Telefone
from shared.types import DiretorId, EscolaId
from shared.exceptions import (
    EscolaJaPossuiDiretorError,
    EscolaNaoEncontradaError,
    PersistenciaError,
)

from .._util import (
    parse_datetime,
    confirmar_transacao,
    obter_id_gerado,
    eh_violacao_unique,
    eh_violacao_foreign_key,
)


class SqliteDiretorRepository(DiretorRepository):
    """
    Persiste Diretores numa tabela SQLite.

    escola_id é UNIQUE no schema (relação 1:1). Um IntegrityError ao
    salvar/atualizar significa uma de duas coisas: a escola já tem
    diretor (UNIQUE) ou o escola_id informado não existe (FOREIGN KEY)
    — as duas mensagens do SQLite são distinguíveis pelo texto.

    Nada referencia diretores.id como chave estrangeira, então
    `remover` não tem cenário de violação de integridade a tratar.
    """

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao

#-----------------------------------------------------------------#

    def salvar(self, diretor: Diretor) -> Diretor:
        try:
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

            confirmar_transacao(self._conexao)

            diretor.id = DiretorId(obter_id_gerado(cursor))
            return diretor

        except sqlite3.IntegrityError as exc:
            if eh_violacao_unique(exc):
                raise EscolaJaPossuiDiretorError() from exc
            if eh_violacao_foreign_key(exc):
                raise EscolaNaoEncontradaError(diretor.escola_id) from exc
            raise PersistenciaError("Falha de integridade ao salvar o Diretor.") from exc

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao salvar o Diretor.") from exc

#-----------------------------------------------------------------#

    def buscar_por_id(self, diretor_id: DiretorId) -> Diretor | None:
        try:
            linha = self._conexao.execute(
                "SELECT * FROM diretores WHERE id = ?", (diretor_id,)
            ).fetchone()

            return self._para_entidade(linha) if linha else None

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao buscar o Diretor.") from exc

#-----------------------------------------------------------------#

    def buscar_por_escola(self, escola_id: EscolaId) -> Diretor | None:
        try:
            linha = self._conexao.execute(
                "SELECT * FROM diretores WHERE escola_id = ?", (escola_id,)
            ).fetchone()

            return self._para_entidade(linha) if linha else None

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao buscar o Diretor da Escola.") from exc

#-----------------------------------------------------------------#

    def listar_todas(self) -> list[Diretor]:
        try:
            linhas = self._conexao.execute(
                "SELECT * FROM diretores ORDER BY id"
            ).fetchall()
            return [self._para_entidade(linha) for linha in linhas]

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao listar os Diretores.") from exc

#-----------------------------------------------------------------#

    def atualizar(self, diretor: Diretor) -> Diretor:
        try:
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

            confirmar_transacao(self._conexao)

            return diretor

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao atualizar o Diretor.") from exc

#-----------------------------------------------------------------#

    def remover(self, diretor_id: DiretorId) -> None:
        try:
            self._conexao.execute("DELETE FROM diretores WHERE id = ?", (diretor_id,))
            confirmar_transacao(self._conexao)

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao remover o Diretor.") from exc

#-----------------------------------------------------------------#

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
