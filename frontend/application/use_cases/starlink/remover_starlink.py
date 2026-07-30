"""
Caso de uso: remover uma designação de Starlink existente.
"""

from __future__ import annotations

from domain.repositories import StarlinkRepository
from shared.exceptions import StarlinkNaoEncontradoError
from shared.types import StarlinkId


class RemoverStarlinkUseCase:
    """
    Remove uma designação de Starlink existente.
    """

    def __init__(self, repositorio: StarlinkRepository) -> None:
        self._repositorio = repositorio

    def executar(self, starlink_id: int) -> None:
        """
        Remove uma designação de Starlink.

        Args:
            starlink_id:
                Identificador da designação.

        Raises:
            StarlinkNaoEncontradoError:
                Caso não exista uma designação com o identificador
                informado.
        """

        starlink_id = StarlinkId(starlink_id)

        starlink = self._repositorio.buscar_por_id(starlink_id)

        if starlink is None:
            raise StarlinkNaoEncontradoError(starlink_id)

        self._repositorio.remover(starlink_id)
