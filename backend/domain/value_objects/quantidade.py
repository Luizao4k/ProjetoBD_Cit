"""
Value Object para representar uma quantidade.
"""

from dataclasses import dataclass

from backend.shared.exceptions import QuantidadeInvalidaError



@dataclass(frozen=True)
class Quantidade:
    """
    Representa uma quantidade inteira positiva.
    """
    valor: int

    def __post_init__(self) -> None:
        if type(self.valor) is not int:
            raise QuantidadeInvalidaError(
                "A quantidade deve ser um número inteiro."
            )

        if self.valor <= 0:
            raise QuantidadeInvalidaError(
                "A quantidade deve ser maior que zero."
            )

    def __int__(self) -> int:
        return self.valor

    def __str__(self) -> str:
        return str(self.valor)
