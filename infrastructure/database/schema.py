"""Decisões técnicas:
  - WAL mode  → melhor concorrência de leitura.
  - Foreign keys ON  → integridade referencial garantida pelo banco.
  - Row factory = Row  → acesso por nome de coluna.
  - CHECK constraints refletem as regras do domain/value_objects.
"""
from __future__ import annotations
import sqlite3

_DDL = """
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------
-- REGIONAL
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dre (
    id_regional    INTEGER PRIMARY KEY AUTOINCREMENT,
    nome           TEXT    NOT NULL,
    municipio_sede TEXT,
    criado_em      TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%S', 'now'))
);

-- ---------------------------------------------------------------
-- ESCOLA
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS escola (
    id_escola     INTEGER PRIMARY KEY AUTOINCREMENT,
    inep          TEXT    NOT NULL UNIQUE,
    nome          TEXT    NOT NULL,
    tipo          TEXT    NOT NULL CHECK (tipo IN ('ESTADUAL', 'MUNICIPAL')),
    regional_id        INTEGER NOT NULL REFERENCES dre(id_dre) ON DELETE RESTRICT,
    municipio     TEXT,
    endereco      TEXT,
    latitude      REAL,
    longitude     REAL,
    contato       TEXT,
    criado_em     TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%S', 'now')),
    atualizado_em TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%S', 'now'))
);

-- ---------------------------------------------------------------
-- DIRETOR  (N diretores por escola, histórico preservado)
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS diretor (
    id_diretor INTEGER PRIMARY KEY AUTOINCREMENT,
    escola_id  INTEGER NOT NULL REFERENCES escola(id_escola) ON DELETE CASCADE,
    nome       TEXT    NOT NULL,
    telefone   TEXT,
    email      TEXT,
    criado_em  TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%S', 'now'))
);

-- ---------------------------------------------------------------
-- CEMEP  (somente escolas MUNICIPAIS — regra aplicada na app layer)
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS cemep (
    id_cemep          INTEGER PRIMARY KEY AUTOINCREMENT,
    escola_id         INTEGER NOT NULL UNIQUE REFERENCES escola(id_escola) ON DELETE CASCADE,
    turma             TEXT,
    nome_responsavel  TEXT,
    observacao        TEXT,
    criado_em         TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%S', 'now')),
    atualizado_em     TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%S', 'now'))
);

-- ---------------------------------------------------------------
-- PROJETO
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS projeto (
    id_projeto INTEGER PRIMARY KEY AUTOINCREMENT,
    nome       TEXT NOT NULL UNIQUE,
    criado_em  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%S', 'now'))
);

-- ---------------------------------------------------------------
-- ESCOLA_PROJETO  (associação N:N com atributos)
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS escola_projeto (
    id_escola_projeto INTEGER PRIMARY KEY AUTOINCREMENT,
    escola_id         INTEGER NOT NULL REFERENCES escola(id_escola)   ON DELETE CASCADE,
    projeto_id        INTEGER NOT NULL REFERENCES projeto(id_projeto)  ON DELETE CASCADE,
    status            TEXT    NOT NULL DEFAULT 'PENDENTE'
                              CHECK (status IN ('ATIVO', 'INATIVO', 'PENDENTE')),
    designacao        TEXT,
    observacao        TEXT,
    criado_em         TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%S', 'now')),
    UNIQUE (escola_id, projeto_id)
);

-- Índices para queries frequentes
CREATE INDEX IF NOT EXISTS idx_escola_dre       ON escola(dre_id);
CREATE INDEX IF NOT EXISTS idx_diretor_escola   ON diretor(escola_id);
CREATE INDEX IF NOT EXISTS idx_cemep_escola     ON cemep(escola_id);
CREATE INDEX IF NOT EXISTS idx_ep_escola        ON escola_projeto(escola_id);
CREATE INDEX IF NOT EXISTS idx_ep_projeto       ON escola_projeto(projeto_id);
"""

def inicializar_schema(conn: sqlite3.Connection) -> None:
    """Executa o DDL completo — idempotente (IF NOT EXISTS)."""
    conn.executescript(_DDL)
    conn.commit()
