"""Erros relacionados aos VO"""

from .base import ValorInvalidoError


class NomeInvalidoError(ValorInvalidoError):
    """Nome inválido."""


class TelefoneInvalidoError(ValorInvalidoError):
    """Telefone inválido."""


class EmailInvalidoError(ValorInvalidoError):
    """Email inválido."""


class MunicipioInvalidoError(ValorInvalidoError):
    """Município inválido."""


class EnderecoInvalidoError(ValorInvalidoError):
    """Endereço inválido."""
