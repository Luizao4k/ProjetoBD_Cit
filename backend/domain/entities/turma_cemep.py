"""
Entidade de domínio: TurmaCemep.
"""

from __future__ import annotations

from dataclasses import dataclass

from backend.domain.value_objects import Nome
from backend.shared.types import TurmaCemepId, ResponsavelId
from .base import AuditoriaEntidade

@dataclass(kw_only=True)
class TurmaCemep(AuditoriaEntidade):
    """
    Representa uma turma vinculada a um responsável do Cemep.
    """

    id: TurmaCemepId | None

    nome_turma: Nome

    responsavel_id: ResponsavelId

    # ------------------------------------------------------------------
    # Regras de negócio
    # ------------------------------------------------------------------

    def alterar_nome(self, nome_turma: Nome) -> None:
        """Função que altera o nome"""
        self.nome_turma = nome_turma
        self._marcar_tempo()
