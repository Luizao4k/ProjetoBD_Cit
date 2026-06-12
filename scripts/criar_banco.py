import sqlite3
import os

# ─────────────────────────────────────────────
# Configuração
# ─────────────────────────────────────────────
NOME_BANCO = "escolas.db"


def criar_banco():
    novo = not os.path.exists(NOME_BANCO)

    conn = sqlite3.connect(NOME_BANCO)
    cursor = conn.cursor()

    # Garante integridade referencial no SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    # ─────────────────────────────────────────
    # Tabela: regional
    # Armazena DREs e NTEs
    # ─────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS regional (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            nome      TEXT    NOT NULL,
            municipio TEXT    NOT NULL,
            tipo      TEXT    NOT NULL CHECK (tipo IN ('DRE', 'NTE')),
            criado_em TEXT    DEFAULT (datetime('now', 'localtime'))
        );
    """)

    # ─────────────────────────────────────────
    # Tabela: escola
    # Cada escola pertence a uma regional
    # ─────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS escola (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            inep                TEXT    NOT NULL UNIQUE,
            nomeEscola          TEXT    NOT NULL,
            regional_id         INTEGER NOT NULL REFERENCES regional(id),
            desigStarlink       TEXT,
            telefone            TEXT,
            diretorResponsavel  TEXT,
            emailDiretor        TEXT,
            criado_em           TEXT    DEFAULT (datetime('now', 'localtime')),
            atualizado_em       TEXT    DEFAULT (datetime('now', 'localtime'))
        );
    """)

    # ─────────────────────────────────────────
    # Tabela: escola
    # Cada escola pertence a uma regional
    # ─────────────────────────────────────────
    cursor.execute ("""
        CREATE TABLE IF NOT EXISTS web_escola (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            escola_id           TEXT    NOT NULL REFERENCES escolas(id) ON DELETE CASCADE,
            ip                  TEXT    NOT NULL,
            criado_em           TEXT    DEFAULT (datetime('now', 'localtime'))
        ); 
    """)

    # ─────────────────────────────────────────
    # Trigger: atualiza campo atualizado_em
    # automaticamente a cada UPDATE na escola
    # ─────────────────────────────────────────
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS atualizar_timestamp
        AFTER UPDATE ON escola
        FOR EACH ROW
        BEGIN
            UPDATE escola
            SET atualizado_em = datetime('now', 'localtime')
            WHERE id = OLD.id;
        END;
    """)

    conn.commit()
    conn.close()

    if novo:
        print(f"✔ Banco '{NOME_BANCO}' criado com sucesso.")
    else:
        print(f"✔ Banco '{NOME_BANCO}' já existia — nenhuma alteração feita.")

    print("  Tabelas: regional, escola, web_escola")
    print("  Trigger: atualizar_timestamp")


# ─────────────────────────────────────────────
# Utilitário: inspecionar o banco criado
# ─────────────────────────────────────────────
def inspecionar_banco():
    if not os.path.exists(NOME_BANCO):
        print("Banco não encontrado. Rode criar_banco() primeiro.")
        return

    conn = sqlite3.connect(NOME_BANCO)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tabelas = cursor.fetchall()

    print(f"\nTabelas em '{NOME_BANCO}':")
    for (tabela,) in tabelas:
        print(f"\n  [{tabela}]")
        cursor.execute(f"PRAGMA table_info({tabela});")
        colunas = cursor.fetchall()
        for col in colunas:
            cid, nome, tipo, notnull, default, pk = col
            flags = []
            if pk:
                flags.append("PK")
            if notnull:
                flags.append("NOT NULL")
            if default is not None:
                flags.append(f"DEFAULT {default}")
            flag_str = "  ← " + ", ".join(flags) if flags else ""
            print(f"    {nome:25} {tipo}{flag_str}")

    conn.close()


# ─────────────────────────────────────────────
# Execução
# ─────────────────────────────────────────────
if __name__ == "__main__":
    criar_banco()
    inspecionar_banco()