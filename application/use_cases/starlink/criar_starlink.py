"""
Caso de uso: criar uma nova designação de Starlink.
"""
from __future__ import annotations

from domain.entities import Starlink
from domain.repositories import StarlinkRepository
from domain.value_objects import Nome

from .dtos import CriarStarlinkInput, StarlinkOutput


class CriarStarlinkUseCase:
    """
    Cria uma nova designação de Starlink vinculada a uma Escola.

    Uma escola pode ter mais de uma designação (relação 1:N).
    """

    def __init__(self, repositorio: StarlinkRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dados: CriarStarlinkInput) -> StarlinkOutput:
        starlink = Starlink(
            id=None,
            escola_id=dados.escola_id,
            designacao=Nome(dados.designacao),
        )

        starlink_criado = self._repositorio.salvar(starlink)

        return StarlinkOutput.de_entidade(starlink_criado)
