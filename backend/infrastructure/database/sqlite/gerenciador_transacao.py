"""
Implementação SQLite do Protocol GerenciadorDeTransacao
(importacao.protocolos).
"""

from __future__ import annotations

import sqlite3

from infrastructure.database.sqlite._util import confirmar_transacao


class GerenciadorDeTransacaoSqlite:
    """
    Confirma ou desfaz uma transação numa conexão SQLite.

    Usado pelo ImportadorPipeline (scripts/importar_*.py) para
    devolver, linha a linha, o mesmo comportamento que os
    repositórios tinham antes de pararem de comitar sozinhos: uma
    linha bem-sucedida é confirmada e se torna permanente antes de a
    próxima linha ser processada — nenhum erro numa linha posterior
    pode desfazer o que já foi salvo.
    """

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conexao = conexao

    def confirmar(self) -> None:
        confirmar_transacao(self._conexao)

    def desfazer(self) -> None:
        self._conexao.rollback()
