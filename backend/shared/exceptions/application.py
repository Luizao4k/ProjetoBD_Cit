"""
Exceções da camada de aplicação.

Representam erros de execução dos casos de uso e regras que
dependem da coordenação entre entidades e repositórios.
"""

from typing import Any

from . import ApplicationError

class RegistroDuplicadoError(ApplicationError):
    """
    Classe base para violação de regra de unicidade.

    Levantada sem argumento (`raise EscolaJaPossuiCemepError()`, como
    já é feito nos repositórios), usa a docstring da própria subclasse
    como mensagem — por isso cada subclasse documenta a regra violada
    numa frase. Ainda aceita uma mensagem explícita se algum dia for
    preciso.
    """

    def __init__(self, mensagem: str | None = None) -> None:
        super().__init__(mensagem or self.__doc__ or "Violação de unicidade.")


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


class EscolaJaPossuiDiretorError(RegistroDuplicadoError):
    """A escola já possui um Diretor cadastrado."""


class EscolaJaPossuiChromebookError(RegistroDuplicadoError):
    """A escola já possui um registro de Chromebook cadastrado."""


class InepJaCadastradoError(RegistroDuplicadoError):
    """Já existe uma Escola cadastrada com esse código INEP."""

class DesignacaoStarlinkDuplicadaError(RegistroDuplicadoError):
    """Indica que a designação de uma Starlink já está cadastrada."""

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
