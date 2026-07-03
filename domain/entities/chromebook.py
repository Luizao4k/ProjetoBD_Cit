"""
Entidade de domínio: Chromebooks.
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.value_objects import Quantidade
from shared.types import EscolaId, ChromebooksId
from .base import AuditoriaEntidade

@dataclass(kw_only=True)
class Chromebook(AuditoriaEntidade):
    """
    Representa a quantidades de chomebooks de uma escola
    """

    id: ChromebooksId | None

    escola_id: EscolaId

    kit_aluno: Quantidade | None = None
    kit_professor: Quantidade | None =  None

    # ------------------------------------------------------------------
    # Regras de negócio
    # ------------------------------------------------------------------

    def alterar_kit_aluno(self, quantidade: Quantidade) -> None:
        """
        Atualiza a quantidade de kits de alunos.
        """
        self.kit_aluno = quantidade
        self._marcar_tempo()

    def alterar_kit_professor(self, quantidade: Quantidade) -> None:
        """
        Atualiza a quantidade de kits de professores.
        """
        self.kit_professor = quantidade
        self._marcar_tempo()
