"""Erros relacionados às entidades."""
from typing import Final

from shared.exceptions.base import ApplicationError



class EntidadeNaoEncontradaError(ApplicationError):
    """
    Lançada quando uma entidade não é encontrada.
    """

    def __init__(self, entidade: str, id_: int | str):
        self.entidade: Final[str] = entidade
        self.id_: Final[int | str] = id_

        super().__init__(f"{entidade} com id '{id_}' não foi encontrada.")


class EntidadeDuplicadaError(ApplicationError):
    """
    Lançada quando já existe uma entidade com determinado campo.
    """

    def __init__(self, entidade: str, campo: str, valor: str):
        self.entidade: Final[str] = entidade
        self.campo: Final[str] = campo
        self.valor: Final[str] = valor

        super().__init__(
            f"Já existe {entidade} com {campo} '{valor}'."
        )

#---------------------------------------#
#--Exceções do caso de uso de Diretor.--#
#---------------------------------------#


class DiretorNaoEncontradoError(ApplicationError):
    """
    Levantada quando um Diretor não é encontrado pelo
    identificador informado.
    """

    def __init__(self, diretor_id: int) -> None:
        super().__init__(f"Diretor com id={diretor_id} não foi encontrado.")
        self.diretor_id = diretor_id

#---------------------------------------#
#--   Exceções do caso de uso de DRE. --#
#---------------------------------------#

class DreNaoEncontradaError(ApplicationError):
    """
    Levantada quando uma DRE não é encontrada pelo identificador
    informado.
    """

    def __init__(self, dre_id: int) -> None:
        super().__init__(f"DRE com id={dre_id} não foi encontrada.")
        self.dre_id = dre_id

#---------------------------------------#
#--  Exceções do caso de uso de CEMEP --#
#---------------------------------------#

class CemepNaoEncontradoError(ApplicationError):
    """
    Levantada quando um Cemep não é encontrado pelo
    identificador informado.
    """

    def __init__(self, cemep_id: int) -> None:
        super().__init__(f"Cemep com id={cemep_id} não foi encontrado.")
        self.cemep_id = cemep_id

class EscolaNaoPossuiCemepError(ApplicationError):
    """
    Levantada quando um Cemep não é encontrado pela
    Escola informada.
    """
    def __init__(self, escola_id: int) -> None:
        super().__init__(f"Escola com id={escola_id} não possui Cemep.")
        self.escola_id = escola_id
