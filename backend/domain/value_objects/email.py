"""
Regras de negócio para endereço de e-mail.
"""

from dataclasses import dataclass
import re

from backend.shared.exceptions import EmailInvalidoError


@dataclass(frozen=True)
class Email:
    """
    Value Object para endereço de e-mail.

    Regras:
    - Remove espaços nas extremidades.
    - Converte para minúsculas.
    - Deve possuir um formato válido.
    """

    valor: str

    _REGEX = re.compile(
        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )

    def __post_init__(self) -> None:
        email = self.valor.strip().lower()

        if not self._REGEX.fullmatch(email):
            raise EmailInvalidoError(
                "Endereço de e-mail inválido."
            )

        object.__setattr__(self, "valor", email)

    def __str__(self) -> str:
        return self.valor
