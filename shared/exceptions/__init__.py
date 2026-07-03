"""Exporta todos os pacotes"""
from .base import DomainError, ValorInvalidoError

from .entidade import (
    EntidadeDuplicadaError,
    EntidadeNaoEncontradaError,
)

from .regra_negocio import RegraDeNegocioVioladaError

from .value_objects import (
    NomeInvalidoError,
    EmailInvalidoError,
    EnderecoInvalidoError,
    MunicipioInvalidoError,
    TelefoneInvalidoError,
)

__all__ = [
    "DomainError",
    "ValorInvalidoError",

    "EntidadeDuplicadaError",
    "EntidadeNaoEncontradaError",

    "RegraDeNegocioVioladaError",

    "NomeInvalidoError",
    "EmailInvalidoError",
    "EnderecoInvalidoError",
    "MunicipioInvalidoError",
    "TelefoneInvalidoError",
]