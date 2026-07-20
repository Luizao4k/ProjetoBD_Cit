"""Erros relacionados aos VO"""

from shared.exceptions.base import DomainError


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

#-----------------------------------------------#
#----Erros relacionados a regras de negocios----#
#-----------------------------------------------#

class RegraDeNegocioVioladaError(DomainError):
    """
    Lançada quando uma regra de negócio é violada.
    """
