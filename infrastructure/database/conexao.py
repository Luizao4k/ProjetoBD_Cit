"""
Esse arquivo resolve um problema específico:
como compartilhar uma única conexão com o banco durante toda uma requisição HTTP,
sem que cada repositório precise abrir a sua própria.
"""
import sqlite3
from pathlib import Path
from flask import Flask, g

DATABASE = Path("escolas.db")


def criar_conexao_db(caminho_db: str | Path) -> sqlite3.Connection:
    """
    Cria e configura uma conexão SQLite.
    Pode ser usada em scripts, testes ou pelo Flask.
    """
    conn = sqlite3.connect(
        str(caminho_db),
        detect_types=sqlite3.PARSE_DECLTYPES
    )

    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")

    return conn


def get_db() -> sqlite3.Connection:
    """
    Retorna a conexão da requisição atual.
    Cria apenas uma conexão por requisição.
    """
    if "db" not in g:
        g.db = criar_conexao_db(DATABASE)

    return g.db


def close_connection(_exception: BaseException | None = None) -> None:
    """
    Fecha a conexão ao final da requisição.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_app(app: Flask) -> None:
    """
    Registra o fechamento automático da conexão.
    """
    app.teardown_appcontext(close_connection)
