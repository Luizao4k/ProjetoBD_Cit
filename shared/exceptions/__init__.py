"""Exporta todos os pacotes"""
from .base import (
    DomainError,
    ApplicationError,
    RegistroNaoEncontradoError,
    RelacaoNaoEncontradaError
)

from .application import (
    PersistenciaInconsistenteError,
    DreNaoEncontradaError,
    EscolaNaoEncontradaError,
    DiretorNaoEncontradoError,
    ChromebookNaoEncontradoError,
    ResponsavelNaoEncontradoError,
    StarlinkNaoEncontradoError,
    TurmaCemepNaoEncontradaError,
    CemepNaoEncontradoError,
    EscolaNaoPossuiCemepError
)

from .domain import (
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
    "RelacaoNaoEncontradaError",
    "RegistroNaoEncontradoError",

    "PersistenciaInconsistenteError",
    "DreNaoEncontradaError",
    "EscolaNaoEncontradaError",
    "DiretorNaoEncontradoError",
    "ChromebookNaoEncontradoError",
    "ResponsavelNaoEncontradoError",
    "StarlinkNaoEncontradoError",
    "TurmaCemepNaoEncontradaError",
    "CemepNaoEncontradoError",
    "EscolaNaoPossuiCemepError",

    "NomeInvalidoError",
    "EmailInvalidoError",
    "EnderecoInvalidoError",
    "MunicipioInvalidoError",
    "TelefoneInvalidoError",
    "ValorInvalidoError"
]