"""
Implementação SQLite do EscolaRepository.
"""

from __future__ import annotations

import sqlite3

from domain.entities import Escola
from domain.enums import TipoEscola
from domain.repositories import EscolaRepository
from domain.value_objects import Endereco, Inep, Municipio, Nome
from shared.types import DreId, EscolaId

from .._util import parse_datetime, obter_lastrowid


class SqliteEscolaRepository(EscolaRepository):
    """
    Persiste Escolas numa tabela SQLite.

    inep e tipo e municipio não entram no UPDATE de `atualizar` porque
    são imutáveis no domínio (Escola não possui alterar_inep /
    alterar_tipo / alterar_municipio).
    """

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao

    def salvar(self, escola: Escola) -> Escola:
        cursor = self._conexao.execute(
            """
            INSERT INTO escolas
                (inep, nome, tipo, municipio, dre_id, endereco, criado_em, atualizado_em)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                escola.inep.valor,
                escola.nome.valor,
                escola.tipo.value,
                escola.municipio.valor,
                escola.dre_id,
                escola.endereco.valor if escola.endereco else None,
                escola.criado_em.isoformat(),
                escola.atualizado_em.isoformat(),
            ),
        )
        self._conexao.commit()
        escola.id = EscolaId(obter_lastrowid(cursor))
        return escola

    def buscar_por_id(self, escola_id: EscolaId) -> Escola | None:
        linha = self._conexao.execute(
            "SELECT * FROM escolas WHERE id = ?", (escola_id,)
        ).fetchone()
        return self._para_entidade(linha) if linha else None

    def buscar_por_nome(self, nome: Nome) -> list[Escola]:
        linhas = self._conexao.execute(
            "SELECT * FROM escolas WHERE nome = ? ORDER BY id", (nome.valor,)
        ).fetchall()
        return [self._para_entidade(linha) for linha in linhas]

    def buscar_por_inep(self, inep: Inep) -> Escola | None:
        linha = self._conexao.execute(
            "SELECT * FROM escolas WHERE inep = ?", (inep.valor,)
        ).fetchone()
        return self._para_entidade(linha) if linha else None

    def buscar_por_municipio(self, municipio: str) -> list[Escola]:
        linhas = self._conexao.execute(
            "SELECT * FROM escolas WHERE municipio = ? ORDER BY id", (municipio,)
        ).fetchall()
        return [self._para_entidade(linha) for linha in linhas]

    def buscar_por_dre(self, dre_id: DreId) -> list[Escola]:
        linhas = self._conexao.execute(
            "SELECT * FROM escolas WHERE dre_id = ? ORDER BY id", (dre_id,)
        ).fetchall()
        return [self._para_entidade(linha) for linha in linhas]

    def listar_todas(self) -> list[Escola]:
        linhas = self._conexao.execute("SELECT * FROM escolas ORDER BY id").fetchall()
        return [self._para_entidade(linha) for linha in linhas]

    def atualizar(self, escola: Escola) -> Escola:
        self._conexao.execute(
            """
            UPDATE escolas
               SET nome = ?, endereco = ?, atualizado_em = ?
             WHERE id = ?
            """,
            (
                escola.nome.valor,
                escola.endereco.valor if escola.endereco else None,
                escola.atualizado_em.isoformat(),
                escola.id,
            ),
        )
        self._conexao.commit()
        return escola

    def remover(self, escola_id: EscolaId) -> None:
        self._conexao.execute("DELETE FROM escolas WHERE id = ?", (escola_id,))
        self._conexao.commit()

    @staticmethod
    def _para_entidade(linha: sqlite3.Row) -> Escola:
        return Escola(
            id=EscolaId(linha["id"]),
            inep=Inep(linha["inep"]),
            nome=Nome(linha["nome"]),
            tipo=TipoEscola(linha["tipo"]),
            municipio=Municipio(linha["municipio"]),
            dre_id=DreId(linha["dre_id"]),
            endereco=Endereco(linha["endereco"]) if linha["endereco"] else None,
            criado_em=parse_datetime(linha["criado_em"]),
            atualizado_em=parse_datetime(linha["atualizado_em"]),
        )
