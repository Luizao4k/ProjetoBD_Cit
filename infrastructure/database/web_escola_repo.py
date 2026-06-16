"""
Esse arquivo implementa os contratos web_escola_repository definido no domain
"""
import sqlite3
from typing import Optional
from domain.entities.web_escola import WebEscola
from domain.repositories.web_escola_repository import WebEscolaRepository


class WebEscolaRepositorySQLite(WebEscolaRepository):
    """
    Implementação concreta do contrato RegionalRepository usando SQLite.
    Recebe a conexão via construtor — não sabe de onde ela veio.
    """
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    # ─────────────────────────────────────────
    # Helpers privados
    # ─────────────────────────────────────────

    def _row_para_web_escola(self, row: sqlite3.Row) -> WebEscola:
        web = WebEscola.__new__(WebEscola)
        web.id_web_escola        = row["id"]
        web.escola_id = row["escola_id"]
        web.ip        = row["ip"]
        web.criado_em = row["criado_em"]
        return web

    # ─────────────────────────────────────────
    # Implementação do contrato
    # ─────────────────────────────────────────

    def salvar(self, web_escola: WebEscola) -> WebEscola:
        cursor = self._conn.execute(
            "INSERT INTO web_escola (escola_id, ip) VALUES (?, ?)",
            (web_escola.escola_id, web_escola.ip),
        )
        self._conn.commit()
        web_escola.id_web_escola = cursor.lastrowid
        return web_escola

    def buscar_por_id(self, id_web_escola: int) -> Optional[WebEscola]:
        row = self._conn.execute(
            "SELECT * FROM web_escola WHERE id = ?", (id_web_escola,)
        ).fetchone()
        return self._row_para_web_escola(row) if row else None

    def listar_por_escola(self, escola_id: int) -> list[WebEscola]:
        rows = self._conn.execute(
            "SELECT * FROM web_escola WHERE escola_id = ? ORDER BY criado_em",
            (escola_id,),
        ).fetchall()
        return [self._row_para_web_escola(r) for r in rows]

    def atualizar(self, web_escola: WebEscola) -> WebEscola:
        self._conn.execute(
            "UPDATE web_escola SET ip = ? WHERE id = ?",
            (web_escola.ip, web_escola.id_web_escola),
        )
        self._conn.commit()
        return web_escola

    def deletar(self, id_web_escola: int) -> bool:
        cursor = self._conn.execute(
            "DELETE FROM web_escola WHERE id = ?", (id_web_escola,)
        )
        self._conn.commit()
        return cursor.rowcount > 0

    def ip_existe_na_escola(
        self, escola_id: int, ip: str, ignorar_id: Optional[int] = None
    ) -> bool:
        if ignorar_id is not None:
            row = self._conn.execute(
                """SELECT COUNT(*) as total FROM web_escola
                   WHERE escola_id = ? AND ip = ? AND id != ?""",
                (escola_id, ip, ignorar_id),
            ).fetchone()
        else:
            row = self._conn.execute(
                """SELECT COUNT(*) as total FROM web_escola
                   WHERE escola_id = ? AND ip = ?""",
                (escola_id, ip),
            ).fetchone()
        return row["total"] > 0
