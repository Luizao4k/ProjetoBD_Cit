"""
Exceções da camada de infraestrutura relacionadas à persistência.
"""

from .base import InfrastructureError


class PersistenciaError(InfrastructureError):
    """Classe base para erros de persistência."""

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
