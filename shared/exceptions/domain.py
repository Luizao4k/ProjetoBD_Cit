"""
Exceções de domínio.

Representam violações das invariantes do domínio detectadas pelas
entidades e Value Objects.
"""

from . import DomainError


class NomeInvalidoError(DomainError):
    """Nome inválido."""


class TelefoneInvalidoError(DomainError):
    """Telefone inválido."""


class EmailInvalidoError(DomainError):
    """E-mail inválido."""


class MunicipioInvalidoError(DomainError):
    """Município inválido."""


class EnderecoInvalidoError(DomainError):
    """Endereço inválido."""


class InepInvalidoError(DomainError):
    """Código INEP inválido."""


class QuantidadeInvalidaError(DomainError):
    """Quantidade inválida."""


class ComentarioInvalidoError(DomainError):
    """Comentário inválido."""
