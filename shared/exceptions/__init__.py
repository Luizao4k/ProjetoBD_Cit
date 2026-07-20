"""Exporta todos os pacotes"""
from .base import DomainError, ApplicationError, PersistenciaInconsistenteError

from .application import (
    EntidadeDuplicadaError,
    EntidadeNaoEncontradaError,
    DiretorNaoEncontradoError,
    DreNaoEncontradaError,
    CemepNaoEncontradoError,
    EscolaNaoPossuiCemepError
)

from .domain import (
    RegraDeNegocioVioladaError,
    NomeInvalidoError,
    EmailInvalidoError,
    EnderecoInvalidoError,
    MunicipioInvalidoError,
    TelefoneInvalidoError,
    ValorInvalidoError
)

__all__ = [
    "DomainError",
    "ApplicationError",
    "PersistenciaInconsistenteError",
    "EscolaNaoPossuiCemepError",

    "EntidadeDuplicadaError",
    "EntidadeNaoEncontradaError",
    "DiretorNaoEncontradoError",
    "DreNaoEncontradaError",
    "CemepNaoEncontradoError",

    "RegraDeNegocioVioladaError",

    "NomeInvalidoError",
    "EmailInvalidoError",
    "EnderecoInvalidoError",
    "MunicipioInvalidoError",
    "TelefoneInvalidoError",
    "ValorInvalidoError"
]