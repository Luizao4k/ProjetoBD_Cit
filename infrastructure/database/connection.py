import sqlite3
from flask import g

DATABASE = "escolas.db"

def get_connection() -> sqlite3.Connection:
    """
    Retorna a conexão ativa do contexto da requisição Flask, se ainda não existir, abre uma nova no g.
    O row_factory permite acessar colunas pelo nome (row["nome"]) em vez de por índice (row[0])
    """
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON;")
    return g.db

def close_connection(exception=None) -> None:
    """
    Fecha a conexão ao fim de cada requisição, chamado automaticamente pelo flask via teardown.
    """
    db = g.pop("db", None)
    if db is not None:
        db.close()



def init_app(app) -> None:
    "Registra o teardown na aplicação flask, chamado uma vez no main.py durate a inicialização"
    app.teardown_appcontext(close_connection)