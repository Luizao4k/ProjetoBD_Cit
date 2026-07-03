"""Erros relacionados a regras de negocios"""
from .base import DomainError


class RegraDeNegocioVioladaError(DomainError):
    """
    Lançada quando uma regra de negócio é violada.
    """