"""
Entidade de domínio: Cemep.
"""
from __future__ import annotations

from dataclasses import dataclass

from shared.types import EscolaId, CemepId
from .base import AuditoriaEntidade


@dataclass(kw_only=True)
class Cemep(AuditoriaEntidade):
    """
    Representa as escolas municipais com turmas cemep
    """
    id: CemepId | None

    escola_id: EscolaId
    comentario: str | None = None

    # ------------------------------------------------------------------
    # Regras de negócio
    # ------------------------------------------------------------------
    def alterar_comentario(self, comentario: str | None) -> None:
        """Altera o comentário/observação livre do Cemep."""
        self.comentario = comentario
        self._marcar_tempo()
