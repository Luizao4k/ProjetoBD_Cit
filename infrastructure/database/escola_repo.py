"""
Esse arquivo implementa os contratos EscolaRepository definido no domain
"""
from datetime import datetime
import sqlite3
from typing import Optional, Any
from domain.entities.escola import Escola
from domain.repositories.escola_repository import EscolaRepository


class EscolaRepositorySQLite(EscolaRepository):
    """
    Implementação concreta do contrato EscolaRepository usando SQLite.
    Recebe a conexão via construtor — não sabe de onde ela veio.
    """

    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    # ─────────────────────────────────────────
    # Helpers privados
    # ─────────────────────────────────────────

    def _row_para_escola(self, row: sqlite3.Row) -> Escola:
        """Converte uma linha do banco em uma entidade Escola."""
        escola = Escola.__new__(Escola)
        escola.id_escola          = row["id_escola"]
        escola.inep               = row["inep"]
        escola.nome_escola         = row["nome_escola"]
        escola.regional_id        = row["regional_id"]
        escola.designacao_starlink      = row["designacao_starlink"]
        escola.web_escola          = bool(row["web_escola"])
        escola.telefone           = row["telefone"]
        escola.diretor_responsavel = row["diretor_responsavel"]
        escola.email_diretor       = row["email_diretor"]
        escola.criado_em          = row["criado_em"]
        escola.atualizado_em      = row["atualizado_em"]
        return escola

    def _construir_filtros(
        self,
        regional_id: Optional[int],
        tipo_regional: Optional[str],
        web_escola: Optional[bool],
        busca: Optional[str],
    ) -> tuple[str, list[Any]]:
        """
        Monta dinamicamente a cláusula WHERE e os parâmetros
        com base nos filtros fornecidos.
        """
        condicoes: list[Any] = []
        params: list[Any] = []

        if regional_id is not None:
            condicoes.append("e.regional_id = ?")
            params.append(regional_id)

        if tipo_regional is not None:
            condicoes.append("r.tipo = ?")
            params.append(tipo_regional)

        if web_escola is not None:
            condicoes.append("e.web_escola = ?")
            params.append(1 if web_escola else 0)

        if busca:
            condicoes.append("(e.nome_escola LIKE ? OR e.inep LIKE ?)")
            termo = f"%{busca}%"
            params.extend([termo, termo])

        where = ("WHERE " + " AND ".join(condicoes)) if condicoes else ""
        return where, params

    # ─────────────────────────────────────────
    # Implementação do contrato
    # ─────────────────────────────────────────

    def salvar(self, escola: Escola) -> Escola:
        cursor = self._conn.execute(
            """
            INSERT INTO escola (
                inep, nome_escola, regional_id, designacao_starlink,
                web_escola, telefone, diretor_responsavel, email_diretor,
                criado_em, atualizado_em
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                escola.inep, escola.nome_escola, escola.regional_id,
                escola.designacao_starlink, int(escola.web_escola),
                escola.telefone, escola.diretor_responsavel, escola.email_diretor,
                escola.criado_em, escola.atualizado_em,
            ),
        )
        self._conn.commit()
        escola.id_escola = cursor.lastrowid
        return escola

    def buscar_por_id(self, id_escola: int) -> Optional[Escola]:
        row = self._conn.execute(
            "SELECT * FROM escola WHERE id_escola = ?", (id_escola,)
        ).fetchone()
        return self._row_para_escola(row) if row else None

    def buscar_por_inep(self, inep: str) -> Optional[Escola]:
        row = self._conn.execute(
            "SELECT * FROM escola WHERE inep = ?", (inep,)
        ).fetchone()
        return self._row_para_escola(row) if row else None

    def buscar_por_regional(self, regional_id: int) -> list[Escola]:
        rows = self._conn.execute(
            "SELECT * FROM escola WHERE regional_id = ? ORDER BY nome_escola",
            (regional_id,),
        ).fetchall()
        return [self._row_para_escola(r) for r in rows]

    def listar_todas(self) -> list[Escola]:
        rows = self._conn.execute(
            "SELECT * FROM escola ORDER BY nome_escola"
        ).fetchall()
        return [self._row_para_escola(r) for r in rows]

    def buscar_com_filtros(
        self,
        regional_id: Optional[int] = None,
        tipo_regional: Optional[str] = None,
        web_escola: Optional[bool] = None,
        busca: Optional[str] = None,
    ) -> list[Escola]:
        where, params = self._construir_filtros(
            regional_id, tipo_regional, web_escola, busca
        )
        rows = self._conn.execute(
            f"""
            SELECT e.*
            FROM escola e
            JOIN regional r ON e.regional_id = r.id
            {where}
            ORDER BY e.nome_escola
            """,
            params,
        ).fetchall()
        return [self._row_para_escola(r) for r in rows]

    def atualizar(self, escola: Escola) -> Escola:
        escola.atualizado_em = datetime.now()
        self._conn.execute(
            """
            UPDATE escola
            SET nome_escola = ?, regional_id = ?, designacao_starlink = ?,
                web_escola = ?, telefone = ?, diretor_responsavel = ?,
                email_diretor = ?, atualizado_em = ?
            WHERE id_escola = ?
            """,
            (
                escola.nome_escola, escola.regional_id, escola.designacao_starlink,
                int(escola.web_escola), escola.telefone,
                escola.diretor_responsavel, escola.email_diretor,
                escola.atualizado_em, escola.id_escola,
            ),
        )
        self._conn.commit()
        return escola

    def deletar(self, id_escola: int) -> bool:
        cursor = self._conn.execute(
            "DELETE FROM escola WHERE id_escola = ?", (id_escola,)
        )
        self._conn.commit()
        return cursor.rowcount > 0

    def inep_existe(self, inep: str, ignorar_id: Optional[int] = None) -> bool:
        if ignorar_id is not None:
            row = self._conn.execute(
                "SELECT COUNT(*) as total FROM escola WHERE inep = ? AND id_escola != ?",
                (inep, ignorar_id),
            ).fetchone()
        else:
            row = self._conn.execute(
                "SELECT COUNT(*) as total FROM escola WHERE inep = ?", (inep,)
            ).fetchone()
        return row["total"] > 0
