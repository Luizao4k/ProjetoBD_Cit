"""
Value Object para telefone.
"""
from __future__ import annotations
import re

from dataclasses import dataclass
from typing import Optional
from shared.exceptions import TelefoneInvalidoError




@dataclass(frozen=True)
class Telefone:
    """
    Regras:
    - Remove caracteres que não são números.
    - Deve possuir entre 8 e 11 dígitos.
    - Um Telefone sempre é válido.
    """

    valor: str

    def __post_init__(self) -> None:
        telefone = re.sub(r"\D", "", self.valor)

        if not 8 <= len(telefone) <= 11:
            raise TelefoneInvalidoError(
                "Telefone deve possuir entre 8 e 11 dígitos."
            )

        object.__setattr__(self, "valor", telefone)

    @classmethod
    def criar(cls, valor: str | None) -> Optional["Telefone"]:
        """
        Cria um telefone válido ou retorna None.

        Retorna:
            Telefone: quando válido.
            None: quando vazio, nulo ou inválido.
        """
        if valor is None:
            return None

        telefone = re.sub(r"\D", "", valor)

        if not 8 <= len(telefone) <= 11:
            return None

        return cls(telefone)

    def __str__(self) -> str:
        return self.valor
