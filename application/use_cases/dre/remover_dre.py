"""
Caso de uso: remover uma DRE existente.
"""
from __future__ import annotations

from shared.types import DreId

from domain.repositories import DreRepository

from .exceptions import DreNaoEncontradaError


class RemoverDreUseCase:
    """
    Remove uma DRE existente pelo identificador.
    """

    def __init__(self, repositorio: DreRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dre_id: DreId) -> None:
        dre = self._repositorio.buscar_por_id(dre_id)

        if dre is None:
            raise DreNaoEncontradaError(dre_id)

        self._repositorio.remover(dre_id)
