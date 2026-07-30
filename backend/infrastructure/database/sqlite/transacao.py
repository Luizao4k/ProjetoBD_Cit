"""
o Context Manager garante automaticamente que a conexão seja aberta,
a transação seja confirmada ou revertida conforme necessário
e os recursos sejam liberados corretamente
"""
from contextlib import contextmanager
from pathlib import Path

from infrastructure.database.sqlite.connection import criar_conexao

@contextmanager
def transacao(
    caminho_banco: str | Path = "escolas.db",
):
    """
    Abre uma conexão SQLite e controla automaticamente
    commit, rollback e fechamento.
    """

    conexao = criar_conexao(caminho_banco)

    try:
        yield conexao

        conexao.commit()

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()
