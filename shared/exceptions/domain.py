""" ---------------------------------------------------------------
# Exceções de domínio (usadas pelos Value Objects em __post_init__)
# ---------------------------------------------------------------"""
from . import DomainError


class NomeInvalidoError(DomainError):
    """Nome inválido."""


class TelefoneInvalidoError(DomainError):
    """Telefone inválido."""


class EmailInvalidoError(DomainError):
    """Email inválido."""


class MunicipioInvalidoError(DomainError):
    """Município inválido."""


class EnderecoInvalidoError(DomainError):
    """Endereço inválido."""

class ValorInvalidoError(DomainError):
    """Valor inválido"""
