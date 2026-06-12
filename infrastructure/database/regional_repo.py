import sqlite3
from typing import Optional
from domain.entities.regional import Regional
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

    def _row_para_regional(self, row: sqlite3.Row) -> Regional:
        """Converte uma linha do banco em uma entidade Regional."""
        regional = Regional.__new__(Regional)
        regional.id        = row["id"]
        regional.nome      = row["nome"]
        regional.municipio = row["municipio"]
        regional.tipo      = row["tipo"]
        regional.criado_em = row["criado_em"]
        return regional

    # ─────────────────────────────────────────
    # Implementação do contrato
    # ─────────────────────────────────────────

    def salvar(self, regional: Regional) -> Regional:
        cursor = self._conn.execute(
            """
            INSERT INTO regional (nome, municipio, tipo)
            VALUES (?, ?, ?)
            """,
            (regional.nome, regional.municipio, regional.tipo),
        )
        self._conn.commit()
        regional.id = cursor.lastrowid
        return regional

    def buscar_por_id(self, id: int) -> Optional[Regional]:
        row = self._conn.execute(
            "SELECT * FROM regional WHERE id = ?", (id,)
        ).fetchone()
        return self._row_para_regional(row) if row else None

    def buscar_por_tipo(self, tipo: str) -> list[Regional]:
        rows = self._conn.execute(
            "SELECT * FROM regional WHERE tipo = ? ORDER BY nome",
            (tipo,),
        ).fetchall()
        return [self._row_para_regional(r) for r in rows]

    def listar_todas(self) -> list[Regional]:
        rows = self._conn.execute(
            "SELECT * FROM regional ORDER BY tipo, nome"
        ).fetchall()
        return [self._row_para_regional(r) for r in rows]

    def atualizar(self, regional: Regional) -> Regional:
        self._conn.execute(
            """
            UPDATE regional
            SET nome = ?, municipio = ?, tipo = ?
            WHERE id = ?
            """,
            (regional.nome, regional.municipio, regional.tipo, regional.id),
        )
        self._conn.commit()
        return regional

    def deletar(self, id: int) -> bool:
        if self.tem_escolas_vinculadas(id):
            raise ValueError(
                f"Não é possível excluir a regional {id} pois "
                "existem escolas vinculadas a ela."
            )
        cursor = self._conn.execute(
            "DELETE FROM regional WHERE id = ?", (id,)
        )
        self._conn.commit()
        return cursor.rowcount > 0

    def tem_escolas_vinculadas(self, id: int) -> bool:
        row = self._conn.execute(
            "SELECT COUNT(*) as total FROM escola WHERE regional_id = ?", (id,)
        ).fetchone()
        return row["total"] > 0