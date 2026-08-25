"""
Entidade de domínio: Responsavel.
"""

from __future__ import annotations

from dataclasses import dataclass

from backend.domain.value_objects import Nome
from backend.shared.types import ResponsavelId, CemepId
from .base import AuditoriaEntidade

@dataclass(kw_only=True)
class Responsavel(AuditoriaEntidade):
    """
    Representa o responsavel pela turma cemep
    """

    id: ResponsavelId | None

    nome: Nome

    cemep_id: CemepId

    # ------------------------------------------------------------------
    # Regras de negócio
    # ------------------------------------------------------------------

    def alterar_nome(self, nome: Nome) -> None:
        """Função que altera o nome"""
        self.nome = nome
        self._marcar_tempo()
