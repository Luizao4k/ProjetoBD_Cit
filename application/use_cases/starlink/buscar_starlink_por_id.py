"""
Caso de uso: buscar uma designação de Starlink pelo identificador.
"""
from __future__ import annotations

from shared.types import StarlinkId

from domain.repositories import StarlinkRepository

from .dtos import StarlinkOutput
from .exceptions import StarlinkNaoEncontradoError


class BuscarStarlinkPorIdUseCase:
    """
    Retorna os dados de uma designação de Starlink a partir do seu
    identificador.
    """

    def __init__(self, repositorio: StarlinkRepository) -> None:
        self._repositorio = repositorio

    def executar(self, starlink_id: StarlinkId) -> StarlinkOutput:
        starlink = self._repositorio.buscar_por_id(starlink_id)

        if starlink is None:
            raise StarlinkNaoEncontradoError(starlink_id)

        return StarlinkOutput.de_entidade(starlink)
