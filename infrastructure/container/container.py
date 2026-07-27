"""
Composition Root da aplicação.

Centraliza a criação da conexão com o banco de dados e disponibiliza
todos os módulos responsáveis por montar os repositórios e casos de
uso da aplicação.
"""

from __future__ import annotations

import sqlite3

from infrastructure.database.sqlite.connection import criar_conexao
from infrastructure.database.sqlite.schema import criar_schema


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
