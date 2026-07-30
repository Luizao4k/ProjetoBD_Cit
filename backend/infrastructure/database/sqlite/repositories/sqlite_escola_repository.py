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
from shared.exceptions import (
    InepJaCadastradoError,
    DreNaoEncontradaError,
    EscolaPossuiDiretorError,
    EscolaPossuiCemepError,
    EscolaPossuiChromebookError,
    EscolaPossuiStarlinksError,
    PersistenciaError,
)

from .._util import (
    parse_datetime,
    confirmar_transacao,
    obter_id_gerado,
    eh_violacao_unique,
    eh_violacao_foreign_key,
)


class SqliteEscolaRepository(EscolaRepository):
    """
    Persiste Escolas numa tabela SQLite.

    inep, tipo e municipio não entram no UPDATE de `atualizar` porque
    são imutáveis no domínio (Escola não possui alterar_inep /
    alterar_tipo / alterar_municipio) — por isso `atualizar` não tem
    cenário de violação de integridade a tratar.

    `remover` é o caso mais delicado do projeto: uma Escola pode ser
    referenciada por 4 tabelas diferentes (diretores, cemeps,
    chromebooks, starlinks), e a mensagem do SQLite para violação de
    FOREIGN KEY não diz qual delas — por isso o diagnóstico explícito
    em `_identificar_bloqueio`.
    """

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao

#-----------------------------------------------------------------#

    def salvar(self, escola: Escola) -> Escola:
        try:
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

            confirmar_transacao(self._conexao)

            escola.id = EscolaId(obter_id_gerado(cursor))
            return escola

        except sqlite3.IntegrityError as exc:
            if eh_violacao_unique(exc):
                raise InepJaCadastradoError() from exc
            if eh_violacao_foreign_key(exc):
                raise DreNaoEncontradaError(escola.dre_id) from exc
            raise PersistenciaError("Falha de integridade ao salvar a Escola.") from exc

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao salvar a Escola.") from exc

#-----------------------------------------------------------------#

    def buscar_por_id(self, escola_id: EscolaId) -> Escola | None:
        try:
            linha = self._conexao.execute(
                "SELECT * FROM escolas WHERE id = ?", (escola_id,)
            ).fetchone()

            return self._para_entidade(linha) if linha else None

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao buscar a Escola.") from exc

#-----------------------------------------------------------------#

    def buscar_por_nome(self, nome: Nome) -> list[Escola]:
        try:
            linhas = self._conexao.execute(
                "SELECT * FROM escolas WHERE nome = ? ORDER BY id", (nome.valor,)
            ).fetchall()
            return [self._para_entidade(linha) for linha in linhas]

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao buscar Escolas por nome.") from exc

#-----------------------------------------------------------------#

    def buscar_por_inep(self, inep: Inep) -> Escola | None:
        try:
            linha = self._conexao.execute(
                "SELECT * FROM escolas WHERE inep = ?", (inep.valor,)
            ).fetchone()

            return self._para_entidade(linha) if linha else None

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao buscar Escola por INEP.") from exc

#-----------------------------------------------------------------#

    def buscar_por_municipio(self, municipio: str) -> list[Escola]:
        try:
            linhas = self._conexao.execute(
                "SELECT * FROM escolas WHERE municipio = ? ORDER BY id", (municipio,)
            ).fetchall()
            return [self._para_entidade(linha) for linha in linhas]

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao buscar Escolas por município.") from exc

#-----------------------------------------------------------------#

    def buscar_por_dre(self, dre_id: DreId) -> list[Escola]:
        try:
            linhas = self._conexao.execute(
                "SELECT * FROM escolas WHERE dre_id = ? ORDER BY id", (dre_id,)
            ).fetchall()
            return [self._para_entidade(linha) for linha in linhas]

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao buscar Escolas por DRE.") from exc

#-----------------------------------------------------------------#

    def listar_todas(self) -> list[Escola]:
        try:
            linhas = self._conexao.execute("SELECT * FROM escolas ORDER BY id").fetchall()
            return [self._para_entidade(linha) for linha in linhas]

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao listar as Escolas.") from exc

#-----------------------------------------------------------------#

    def atualizar(self, escola: Escola) -> Escola:
        try:
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

            confirmar_transacao(self._conexao)

            return escola

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao atualizar a Escola.") from exc

#-----------------------------------------------------------------#

    def remover(self, escola_id: EscolaId) -> None:
        try:
            self._conexao.execute("DELETE FROM escolas WHERE id = ?", (escola_id,))
            confirmar_transacao(self._conexao)

        except sqlite3.IntegrityError as exc:
            raise self._identificar_bloqueio(escola_id) from exc

        except sqlite3.DatabaseError as exc:
            raise PersistenciaError("Falha ao remover a Escola.") from exc

#-----------------------------------------------------------------#

    def _identificar_bloqueio(self, escola_id: EscolaId) -> Exception:
        """
        Descobre qual tabela está impedindo a remoção da Escola.

        Só é chamado depois de um IntegrityError real. A mensagem do
        SQLite ("FOREIGN KEY constraint failed") é genérica demais pra
        dizer sozinha qual das 4 tabelas é a responsável, então cada
        uma é checada explicitamente, na ordem em que a Escola costuma
        ser preenchida (Diretor, CEMEP, Chromebook, Starlink).
        """
        if self._conexao.execute(
            "SELECT 1 FROM diretores WHERE escola_id = ? LIMIT 1", (escola_id,)
        ).fetchone():
            return EscolaPossuiDiretorError()

        if self._conexao.execute(
            "SELECT 1 FROM cemeps WHERE escola_id = ? LIMIT 1", (escola_id,)
        ).fetchone():
            return EscolaPossuiCemepError()

        if self._conexao.execute(
            "SELECT 1 FROM chromebooks WHERE escola_id = ? LIMIT 1", (escola_id,)
        ).fetchone():
            return EscolaPossuiChromebookError()

        if self._conexao.execute(
            "SELECT 1 FROM starlinks WHERE escola_id = ? LIMIT 1", (escola_id,)
        ).fetchone():
            return EscolaPossuiStarlinksError()

        return PersistenciaError(
            "Falha de integridade ao remover a Escola (motivo não identificado)."
        )

#-----------------------------------------------------------------#

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
