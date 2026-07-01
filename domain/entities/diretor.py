"""
Entidade de domínio: Diretor.
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.value_objects import Nome, Telefone, Email
from shared.types import DiretorId
from .base import AuditoriaEntidade

@dataclass
class Diretor(AuditoriaEntidade):
    """
    Representa o diretor atual de uma escola.
    """

    id: DiretorId | None

    nome: Nome
    telefone: Telefone | None = None
    email: Email | None = None

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
