"""
Value Object que representa o código INEP de uma escola.
"""
from dataclasses import dataclass

from shared.exceptions import InepInvalidoError


@dataclass(frozen=True)
class Inep:
    """
    Regras:
    - Deve conter exatamente 8 dígitos numéricos.
    - É imutável.
    """
    valor: str

    def __post_init__(self) -> None:
        if not self.valor.isdigit() or len(self.valor) != 8:
            raise InepInvalidoError(
                f"INEP deve ter exatamente 8 dígitos numéricos. "
                f"Recebido: '{self.valor}'"
            )

    def __str__(self) -> str:
        return self.valor
