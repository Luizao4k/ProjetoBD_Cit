"""
Exceções base do domínio.

Todas as exceções específicas do domínio devem herdar de DomainError.
"""
from __future__ import annotations


class DomainError(Exception):
    """Classe base para erros do domínio."""


class ApplicationError(Exception):
    """Classe base para erros de Value Objects."""

class RelacaoNaoEncontradaError(ApplicationError):
    """
    Classe base para erros de relação 1:1 ausente (ex: escola sem
    diretor cadastrado). Cada subclasse só precisa definir o
    atributo de classe `entidade`.
    """

    entidade: str = "registro relacionado"

    def __init__(self, escola_id: object) -> None:
        super().__init__(
            f"A escola com id={escola_id} não possui "
            f"{self.entidade} cadastrado(a)."
        )
        self.escola_id = escola_id

class RegistroNaoEncontradoError(ApplicationError):
    """
    Classe base para erros de "registro não encontrado pelo id"
    de qualquer entidade. Cada subclasse só precisa definir o
    atributo de classe `entidade`.
    """

    entidade: str = "Registro"

    def __init__(self, identificador: object) -> None:
        super().__init__(
            f"{self.entidade} com id={identificador} não foi encontrado(a)."
        )
        self.identificador = identificador
