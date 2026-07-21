"""Erros relacionados às entidades."""
# ---------------------------------------------------------------
# Exceções de aplicação (usadas pelos casos de uso)
# ---------------------------------------------------------------

from . import ApplicationError, RegistroNaoEncontradoError, RelacaoNaoEncontradaError



class PersistenciaInconsistenteError(ApplicationError):
    """
    Levantada quando o repositório retorna uma entidade em estado
    inconsistente com o que se espera após uma operação de
    persistência (ex: id ainda None depois de salvar/atualizar).

    Indica um bug na implementação concreta do repositório, não
    um erro de uso da aplicação — por isso não deve ser tratada
    como "entrada inválida do usuário".
    """

#--------------------------------------------------------#

class DreNaoEncontradaError(RegistroNaoEncontradoError):
    """ registro não encontrado pelo id de DRE"""
    entidade = "DRE"


class EscolaNaoEncontradaError(RegistroNaoEncontradoError):
    """ registro não encontrado pelo id de Escola"""
    entidade = "Escola"


class DiretorNaoEncontradoError(RegistroNaoEncontradoError):
    """ registro não encontrado pelo id de Diretor"""
    entidade = "Diretor"


class CemepNaoEncontradoError(RegistroNaoEncontradoError):
    """ registro não encontrado pelo id de CEMEP"""
    entidade = "Cemep"


class ChromebookNaoEncontradoError(RegistroNaoEncontradoError):
    """ registro não encontrado pelo id de Chromebook"""
    entidade = "Chromebook"


class ResponsavelNaoEncontradoError(RegistroNaoEncontradoError):
    """ registro não encontrado pelo id de Responsavel"""
    entidade = "Responsavel"


class StarlinkNaoEncontradoError(RegistroNaoEncontradoError):
    """ registro não encontrado pelo id de starlink"""
    entidade = "Starlink"


class TurmaCemepNaoEncontradaError(RegistroNaoEncontradoError):
    """ registro não encontrado pelo id de turma cemep"""
    entidade = "TurmaCemep"


#--------------------------------------------------------#

class EscolaNaoPossuiDiretorError(RelacaoNaoEncontradaError):
    """Relação não encontrada entre entidades"""
    entidade = "diretor"


class EscolaNaoPossuiCemepError(RelacaoNaoEncontradaError):
    """Relação não encontrada entre entidades"""

    entidade = "Cemep"


class EscolaNaoPossuiChromebookError(RelacaoNaoEncontradaError):
    """Relação não encontrada entre entidades"""
    entidade = "registro de Chromebook"
