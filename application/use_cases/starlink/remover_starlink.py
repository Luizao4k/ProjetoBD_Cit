"""
Caso de uso: remover uma designação de Starlink existente.
"""
from __future__ import annotations

from shared.types import StarlinkId

from domain.repositories import StarlinkRepository

from .exceptions import StarlinkNaoEncontradoError


class RemoverStarlinkUseCase:
    """
    Remove uma designação de Starlink existente pelo identificador.
    """

    def __init__(self, repositorio: StarlinkRepository) -> None:
        self._repositorio = repositorio

    def executar(self, starlink_id: StarlinkId) -> None:
        starlink = self._repositorio.buscar_por_id(starlink_id)

        if starlink is None:
            raise StarlinkNaoEncontradoError(starlink_id)

        self._repositorio.remover(starlink_id)
