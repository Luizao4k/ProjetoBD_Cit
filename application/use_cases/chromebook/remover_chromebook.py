"""
Caso de uso: remover um registro de Chromebook existente.
"""
from __future__ import annotations

from shared.types import ChromebooksId

from domain.repositories import ChromebookRepository

from .exceptions import ChromebookNaoEncontradoError


class RemoverChromebookUseCase:
    """
    Remove um registro de Chromebook existente pelo identificador.
    """

    def __init__(self, repositorio: ChromebookRepository) -> None:
        self._repositorio = repositorio

    def executar(self, chromebook_id: ChromebooksId) -> None:
        chromebook = self._repositorio.buscar_por_id(chromebook_id)

        if chromebook is None:
            raise ChromebookNaoEncontradoError(chromebook_id)

        self._repositorio.remover(chromebook_id)
