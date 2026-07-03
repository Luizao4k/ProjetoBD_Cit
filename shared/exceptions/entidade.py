"""Erros relacionados às entidades."""
from typing import Final

from .base import DomainError


class EntidadeNaoEncontradaError(DomainError):
    """
    Lançada quando uma entidade não é encontrada.
    """

    def __init__(self, entidade: str, id_: int | str):
        self.entidade: Final[str] = entidade
        self.id_: Final[int | str] = id_

        super().__init__(f"{entidade} com id '{id_}' não foi encontrada.")


class EntidadeDuplicadaError(DomainError):
    """
    Lançada quando já existe uma entidade com determinado campo.
    """

    def __init__(self, entidade: str, campo: str, valor: str):
        self.entidade: Final[str] = entidade
        self.campo: Final[str] = campo
        self.valor: Final[str] = valor

        super().__init__(
            f"Já existe {entidade} com {campo} '{valor}'."
        )
