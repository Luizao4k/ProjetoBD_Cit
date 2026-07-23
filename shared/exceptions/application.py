"""
Exceções da camada de aplicação.

Representam erros de execução dos casos de uso e regras que
dependem da coordenação entre entidades e repositórios.
"""

from typing import Any

from . import ApplicationError

class RegistroDuplicadoError(ApplicationError):
    """Violação de uma regra de unicidade."""


class RegistroNaoEncontradoError(ApplicationError):
    """
    Classe base para erros de "registro não encontrado pelo id"
    de qualquer entidade. Cada subclasse só precisa definir o
    atributo de classe `entidade`.
    """

    entidade: str = "Registro"

    def __init__(self, identificador: Any) -> None:
        super().__init__(
            f"{self.entidade} com id={identificador} não foi encontrado(a)."
        )
        self.identificador = identificador

class RelacaoNaoEncontradaError(ApplicationError):
    """
    Classe base para erros de relação 1:1 ausente (ex: escola sem
    diretor cadastrado). Cada subclasse só precisa definir o
    atributo de classe `entidade`.
    """

    entidade: str = "registro relacionado"

    def __init__(self, identificador: Any) -> None:
        super().__init__(
            f"A escola com id={identificador} não possui "
            f"{self.entidade} cadastrado(a)."
        )
        self.escola_id = identificador
#--------------------------------------------------------#
#--------------------------------------------------------#
#--------------------------------------------------------#

class EscolaJaPossuiCemepError(RegistroDuplicadoError):
    """A escola já possui um CEMEP cadastrado."""

#------------------------------------------------------#
#------------------------------------------------------#

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

#------------------------------------------------------#
#------------------------------------------------------#

class EscolaNaoPossuiDiretorError(RelacaoNaoEncontradaError):
    """Relação não encontrada entre entidades"""
    entidade = "diretor"


class EscolaNaoPossuiCemepError(RelacaoNaoEncontradaError):
    """Relação não encontrada entre entidades"""

    entidade = "Cemep"


class EscolaNaoPossuiChromebookError(RelacaoNaoEncontradaError):
    """Relação não encontrada entre entidades"""
    entidade = "registro de Chromebook"
