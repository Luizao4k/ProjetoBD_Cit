"""
Entidade de domínio: DRE.
"""
from __future__ import annotations


from dataclasses import dataclass

from backend.shared.types import DreId
from backend.domain.value_objects import  Nome, Telefone
from .base import AuditoriaEntidade


@dataclass(kw_only=True)
class Dre(AuditoriaEntidade):
    """
    Diretoria Regional de Ensino.
    Uma DRE agrupa várias escolas de uma região.
    """

    id: DreId | None
    nome: Nome
    telefone: Telefone | None

    # ------------------------------------------------------------------
    # Regras de negócio
    # ------------------------------------------------------------------

    def alterar_nome(self, nome: Nome) -> None:
        """
        Atualiza o nome da DRE.
        """
        self.nome = nome
        self._marcar_tempo()

    def alterar_telefone(self, telefone: Telefone | None) -> None:
        """
        Atualiza o telefone da DRE.
        """
        self.telefone = telefone
        self._marcar_tempo()
