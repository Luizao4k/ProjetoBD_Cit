"""
Exceções da camada de infraestrutura relacionadas à persistência.
"""

from .base import InfrastructureError


class PersistenciaError(InfrastructureError):
    """
    Classe base para erros de persistência.

    Levantada sem argumento (`raise DrePossuiEscolasError()`, como já é
    feito nos repositórios), usa a docstring da própria subclasse como
    mensagem. Continua aceitando uma mensagem explícita normalmente
    (`raise PersistenciaError("Falha ao salvar...")`), que é como a
    própria classe base costuma ser levantada.
    """

    def __init__(self, mensagem: str | None = None) -> None:
        super().__init__(mensagem or self.__doc__ or "Falha de persistência.")

#--------------------------------------------------------#
#--------------------------------------------------------#
#--------------------------------------------------------#
class PersistenciaInconsistenteError(PersistenciaError):
    """
    O repositório retornou uma entidade em estado inconsistente após
    uma operação de persistência.

    Exemplo:
        - id continua None após salvar;
        - registro recém-salvo não pode ser recuperado;
        - dados retornados pelo banco são incompatíveis com a entidade.

    Indica um erro na implementação da infraestrutura.
    """

class ConexaoBancoError(PersistenciaError):
    """Falha na conexão com o banco de dados."""


class FalhaAoObterIdGeradoError(PersistenciaError):
    """O banco não retornou o identificador gerado."""


class TransacaoError(PersistenciaError):
    """Falha durante a execução de uma transação."""

class CemepPossuiResponsaveisError(PersistenciaError):
    """uma violação de chave estrangeira porque existe
            Responsavel vinculados ao CEMEP"""


class DrePossuiEscolasError(PersistenciaError):
    """Violação de chave estrangeira: existem Escolas vinculadas à DRE."""


class ResponsavelPossuiTurmasError(PersistenciaError):
    """Violação de chave estrangeira: existem Turmas CEMEP vinculadas ao Responsável."""


class EscolaPossuiDiretorError(PersistenciaError):
    """Violação de chave estrangeira: a Escola possui um Diretor vinculado."""


class EscolaPossuiCemepError(PersistenciaError):
    """Violação de chave estrangeira: a Escola possui um CEMEP vinculado."""


class EscolaPossuiChromebookError(PersistenciaError):
    """Violação de chave estrangeira: a Escola possui um registro de Chromebook vinculado."""


class EscolaPossuiStarlinksError(PersistenciaError):
    """Violação de chave estrangeira: a Escola possui designações de Starlink vinculadas."""
