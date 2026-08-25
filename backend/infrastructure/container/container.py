"""
Composition Root da aplicação.

Centraliza a criação da conexão com o banco de dados e disponibiliza
todos os módulos responsáveis por montar os repositórios e casos de
uso da aplicação.
"""

from __future__ import annotations

import sqlite3

from backend.infrastructure.database.sqlite.connection import criar_conexao
from backend.infrastructure.database.sqlite.schema import criar_schema
from backend.infrastructure.database.sqlite._util import confirmar_transacao


from .cemep_modulo import CemepModulo
from .chromebook_modulo import ChromebookModulo
from .diretor_modulo import DiretorModulo
from .dre_modulo import DreModulo
from .escola_modulo import EscolaModulo
from .responsavel_modulo import ResponsavelModulo
from .starlink_modulo import StarlinkModulo
from .turma_cemep_modulo import TurmaCemepModulo


class Container(
    DreModulo,
    EscolaModulo,
    DiretorModulo,
    CemepModulo,
    ChromebookModulo,
    ResponsavelModulo,
    TurmaCemepModulo,
    StarlinkModulo,
):
    """
    Composition Root da aplicação.

    Responsável por criar a conexão com o banco de dados e compor
    todas as dependências necessárias para a execução dos casos de
    uso da aplicação.

    Cada módulo disponibiliza um conjunto de repositórios e casos de
    uso relacionados a uma entidade do domínio.
    """

    def __init__(self, caminho_banco: str = "escolas.db") -> None:
        """
        Inicializa o Container da aplicação.

        Cria a conexão com o banco de dados SQLite, garante que o
        schema esteja atualizado e disponibiliza essa conexão para
        todos os módulos do Container.

        Args:
            caminho_banco:
                Caminho do arquivo do banco SQLite. Utilize
                ``":memory:"`` para testes em memória.
        """
        self._conexao: sqlite3.Connection = criar_conexao(caminho_banco)
        criar_schema(self._conexao)

    def finalizar(self, sucesso: bool) -> None:
        """
        Encerra o ciclo de vida deste Container: confirma ou desfaz a
        transação pendente e fecha a conexão.

        Existe para quem gerencia um Container por fora com um ciclo
        de vida próprio (ex: a API REST, um Container por requisição
        HTTP). Os scripts de importação (Fase 4) não usam Container —
        eles montam os repositórios diretamente e controlam sua
        própria transação por linha via
        infrastructure.database.sqlite.gerenciador_transacao.

        Desde que os repositórios pararam de comitar sozinhos a cada
        escrita (ver infrastructure/database/sqlite/_util.py), este
        método é o único ponto em que uma escrita feita através de um
        Container realmente se torna permanente.

        Args:
            sucesso:
                True confirma (commit) as alterações pendentes; False
                desfaz (rollback). Passar False é o comportamento
                correto quando a requisição terminou por uma exceção.
        """
        if sucesso:
            confirmar_transacao(self._conexao)
        else:
            self._conexao.rollback()

        self._conexao.close()
