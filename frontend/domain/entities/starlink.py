"""
Entidade de domínio: Starlink.
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.value_objects import Nome
from shared.types import EscolaId, StarlinkId
from .base import AuditoriaEntidade

@dataclass(kw_only=True)
class Starlink(AuditoriaEntidade):
    """
    Representa uma designação de Starlink vinculada a uma escola.
    """

    id: StarlinkId | None

    designacao: Nome

    escola_id: EscolaId

    # ------------------------------------------------------------------
    # Regras de negócio
    # ------------------------------------------------------------------

    def alterar_designacao(self, designacao: Nome) -> None:
        """Função que altera a designaçao"""
        self.designacao = designacao
        self._marcar_tempo()
