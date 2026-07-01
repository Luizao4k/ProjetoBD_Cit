"""
Esse arquivo implementa os contratos RegionalRepository definido no domain
"""
import sqlite3
from typing import Optional
from domain.entities.dre import Dre
from domain.repositories.regional_repository import RegionalRepository


class RegionalRepositorySQLite(RegionalRepository):
    """
    Implementação concreta do contrato RegionalRepository usando SQLite.
    Recebe a conexão via construtor — não sabe de onde ela veio.
    """

    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    # ─────────────────────────────────────────
    # Helpers privados
    # ─────────────────────────────────────────

    def _row_para_regional(self, row: sqlite3.Row) -> Dre:
        """Converte uma linha do banco em uma entidade Regional."""
        regional = Dre.__new__(Dre)
        regional.regional_id        = row["id"]
        regional.nome      = row["nome"]
        regional.municipio = row["municipio"]
        regional.tipo      = row["tipo"]
        regional.criado_em = row["criado_em"]
        return regional

    # ─────────────────────────────────────────
    # Implementação do contrato
    # ─────────────────────────────────────────

    def salvar(self, regional: Dre) -> Dre:
        cursor = self._conn.execute(
            """
            INSERT INTO regional (nome, municipio, tipo)
            VALUES (?, ?, ?)
            """,
            (regional.nome, regional.municipio, regional.tipo),
        )
        self._conn.commit()
        regional.regional_id = cursor.lastrowid
        return regional

    def buscar_por_id(self, regional_id: int) -> Optional[Dre]:
        row = self._conn.execute(
            "SELECT * FROM regional WHERE id = ?", (regional_id,)
        ).fetchone()
        return self._row_para_regional(row) if row else None

    def buscar_por_tipo(self, tipo: str) -> list[Dre]:
        rows = self._conn.execute(
            "SELECT * FROM regional WHERE tipo = ? ORDER BY nome",
            (tipo,),
        ).fetchall()
        return [self._row_para_regional(r) for r in rows]

    def listar_todas(self) -> list[Dre]:
        rows = self._conn.execute(
            "SELECT * FROM regional ORDER BY tipo, nome"
        ).fetchall()
        return [self._row_para_regional(r) for r in rows]

    def atualizar(self, regional: Dre) -> Dre:
        self._conn.execute(
            """
            UPDATE regional
            SET nome = ?, municipio = ?, tipo = ?
            WHERE id = ?
            """,
            (regional.nome, regional.municipio, regional.tipo, regional.regional_id),
        )
        self._conn.commit()
        return regional

    def deletar(self, regional_id: int) -> bool:
        if self.tem_escolas_vinculadas(regional_id):
            raise ValueError(
                f"Não é possível excluir a regional {regional_id} pois "
                "existem escolas vinculadas a ela."
            )
        cursor = self._conn.execute(
            "DELETE FROM regional WHERE id = ?", (regional_id,)
        )
        self._conn.commit()
        return cursor.rowcount > 0

    def tem_escolas_vinculadas(self, regional_id: int) -> bool:
        row = self._conn.execute(
            "SELECT COUNT(*) as total FROM escola WHERE regional_id = ?", (regional_id,)
        ).fetchone()
        return row["total"] > 0
