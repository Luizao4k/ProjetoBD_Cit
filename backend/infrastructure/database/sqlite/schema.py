# ---------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------
# Datas (criado_em / atualizado_em) são guardadas como TEXT no formato
# ISO 8601 (ex: "2026-07-23T14:32:10.123456+00:00"), gerado por
# datetime.isoformat() e lido de volta com datetime.fromisoformat().
#
# escola_id é UNIQUE em diretores/cemeps/chromebooks porque essas são
# relações 1:1 com Escola no domínio (ver CriarDiretorUseCase: "a
# verificação de unicidade é responsabilidade da camada de
# persistência"). Uma tentativa de criar um segundo registro para a
# mesma escola faz o SQLite levantar sqlite3.IntegrityError — o projeto
# ainda não tem uma exceção de domínio própria para esse caso (ver
# observações da revisão), então por enquanto ela sobe sem tradução.

import sqlite3

from shared.exceptions import PersistenciaError

SCHEMA = """

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS dres (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    nome          TEXT NOT NULL,
    telefone      TEXT,
    criado_em     TEXT NOT NULL,
    atualizado_em TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS escolas (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    inep          TEXT NOT NULL UNIQUE,
    nome          TEXT NOT NULL,
    tipo          TEXT NOT NULL,
    municipio     TEXT NOT NULL,
    dre_id        INTEGER NOT NULL REFERENCES dres(id),
    endereco      TEXT,
    criado_em     TEXT NOT NULL,
    atualizado_em TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS diretores (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    escola_id     INTEGER NOT NULL UNIQUE REFERENCES escolas(id),
    nome          TEXT NOT NULL,
    telefone      TEXT,
    email         TEXT,
    criado_em     TEXT NOT NULL,
    atualizado_em TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cemeps (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    escola_id     INTEGER NOT NULL UNIQUE REFERENCES escolas(id),
    comentario    TEXT,
    criado_em     TEXT NOT NULL,
    atualizado_em TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS chromebooks (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    escola_id     INTEGER NOT NULL UNIQUE REFERENCES escolas(id),
    kit_aluno     INTEGER,
    kit_professor INTEGER,
    criado_em     TEXT NOT NULL,
    atualizado_em TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS responsaveis (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    cemep_id       INTEGER NOT NULL REFERENCES cemeps(id),
    nome           TEXT NOT NULL,
    criado_em      TEXT NOT NULL,
    atualizado_em  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS turmas_cemep (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    responsavel_id INTEGER NOT NULL REFERENCES responsaveis(id),
    nome_turma     TEXT NOT NULL,
    criado_em      TEXT NOT NULL,
    atualizado_em  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS starlinks (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    escola_id     INTEGER NOT NULL REFERENCES escolas(id),
    designacao    TEXT NOT NULL,
    criado_em     TEXT NOT NULL,
    atualizado_em TEXT NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_starlinks_designacao
ON starlinks(designacao);

CREATE INDEX IF NOT EXISTS ix_escolas_dre_id
ON escolas(dre_id);

CREATE INDEX IF NOT EXISTS ix_responsaveis_cemep_id
ON responsaveis(cemep_id);

CREATE INDEX IF NOT EXISTS ix_turmas_cemep_responsavel_id
ON turmas_cemep(responsavel_id);

CREATE INDEX IF NOT EXISTS ix_starlinks_escola_id
ON starlinks(escola_id);
"""

def criar_schema(conexao: sqlite3.Connection) -> None:
    """Cria Schema do BD"""
    try:
        conexao.executescript(SCHEMA)
        conexao.commit()

    except sqlite3.Error as exc:
        conexao.rollback()
        raise PersistenciaError(
            "Falha ao criar o schema."
        ) from exc
