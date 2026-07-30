"""
Value Object para representar um comentário.
"""

from dataclasses import dataclass

from shared.exceptions import ComentarioInvalidoError
from .. import MAX_LEN


@dataclass(frozen=True)
class Comentario:
    """
    Value Object para comentários curtos.
    """
    valor: str

    def __post_init__(self) -> None:
        valor = self.valor.strip()

        if not valor:
            raise ComentarioInvalidoError(
                "O comentário não pode ser vazio."
            )

        if len(valor) > MAX_LEN:
            raise ComentarioInvalidoError(
                f"O comentário deve ter no máximo {MAX_LEN} caracteres."
            )

        object.__setattr__(self, "valor", valor)

    def __str__(self) -> str:
        return self.valor
