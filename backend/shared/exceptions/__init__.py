"""
Exceções utilizadas pela aplicação.

Organizadas por camada:
- base: exceções base da arquitetura;
- domain: violações das regras de domínio;
- application: erros dos casos de uso;
- infrastructure: erros técnicos da infraestrutura.
"""

from .base import (
    DomainError,
    ApplicationError,
    InfrastructureError,
)

from .domain import (
    NomeInvalidoError,
    TelefoneInvalidoError,
    EmailInvalidoError,
    MunicipioInvalidoError,
    EnderecoInvalidoError,
    InepInvalidoError,
    QuantidadeInvalidaError,
    ComentarioInvalidoError,
)

from .application import (
    RegistroDuplicadoError,
    RegistroNaoEncontradoError,
    RelacaoNaoEncontradaError,
    EscolaJaPossuiCemepError,
    EscolaJaPossuiDiretorError,
    EscolaJaPossuiChromebookError,
    DesignacaoStarlinkDuplicadaError,
    InepJaCadastradoError,
    DreNaoEncontradaError,
    EscolaNaoEncontradaError,
    DiretorNaoEncontradoError,
    CemepNaoEncontradoError,
    ChromebookNaoEncontradoError,
    ResponsavelNaoEncontradoError,
    StarlinkNaoEncontradoError,
    TurmaCemepNaoEncontradaError,
    EscolaNaoPossuiDiretorError,
    EscolaNaoPossuiCemepError,
    EscolaNaoPossuiChromebookError,
)

from .infrastructure import (
    PersistenciaError,
    PersistenciaInconsistenteError,
    ConexaoBancoError,
    FalhaAoObterIdGeradoError,
    TransacaoError,
    CemepPossuiResponsaveisError,
    DrePossuiEscolasError,
    ResponsavelPossuiTurmasError,
    EscolaPossuiDiretorError,
    EscolaPossuiCemepError,
    EscolaPossuiChromebookError,
    EscolaPossuiStarlinksError,
)

__all__ = [
    # Base
    "DomainError",
    "ApplicationError",
    "InfrastructureError",

    # Domain
    "NomeInvalidoError",
    "TelefoneInvalidoError",
    "EmailInvalidoError",
    "MunicipioInvalidoError",
    "EnderecoInvalidoError",
    "InepInvalidoError",
    "QuantidadeInvalidaError",
    "ComentarioInvalidoError",

    # Application
    "RegistroDuplicadoError",
    "RegistroNaoEncontradoError",
    "RelacaoNaoEncontradaError",
    "EscolaJaPossuiCemepError",
    "EscolaJaPossuiDiretorError",
    "EscolaJaPossuiChromebookError",
    "DesignacaoStarlinkDuplicadaError",
    "InepJaCadastradoError",
    "DreNaoEncontradaError",
    "EscolaNaoEncontradaError",
    "DiretorNaoEncontradoError",
    "CemepNaoEncontradoError",
    "ChromebookNaoEncontradoError",
    "ResponsavelNaoEncontradoError",
    "StarlinkNaoEncontradoError",
    "TurmaCemepNaoEncontradaError",
    "EscolaNaoPossuiDiretorError",
    "EscolaNaoPossuiCemepError",
    "EscolaNaoPossuiChromebookError",

    # Infrastructure
    "PersistenciaError",
    "PersistenciaInconsistenteError",
    "ConexaoBancoError",
    "FalhaAoObterIdGeradoError",
    "TransacaoError",
    "CemepPossuiResponsaveisError",
    "DrePossuiEscolasError",
    "ResponsavelPossuiTurmasError",
    "EscolaPossuiDiretorError",
    "EscolaPossuiCemepError",
    "EscolaPossuiChromebookError",
    "EscolaPossuiStarlinksError",
]