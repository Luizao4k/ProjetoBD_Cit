"""
Entidade de domínio: Diretor.
"""

from __future__ import annotations

from dataclasses import dataclass

from backend.domain.value_objects import Nome, Telefone, Email
from backend.shared.types import DiretorId, EscolaId
from .base import AuditoriaEntidade

@dataclass(kw_only=True)
class Diretor(AuditoriaEntidade):
    """
    Representa o diretor atual de uma escola.
    """

    id: DiretorId | None

    escola_id: EscolaId
    nome: Nome
    telefone: Telefone | None = None
    email: Email | None = None

    # ------------------------------------------------------------------
    # Regras de negócio
    # ------------------------------------------------------------------

    def alterar_nome(self, nome: Nome) -> None:
        """Função que altera o nome"""
        self.nome = nome
        self._marcar_tempo()

    def alterar_telefone(self, telefone: Telefone | None) -> None:
        """Função que altera o telefone"""
        self.telefone = telefone
        self._marcar_tempo()

    def alterar_email(self, email: Email | None) -> None:
        """função que altera telefone"""
        self.email = email
        self._marcar_tempo()
