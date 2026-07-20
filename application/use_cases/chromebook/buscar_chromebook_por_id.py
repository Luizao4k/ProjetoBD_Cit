"""
Caso de uso: buscar um registro de Chromebook pelo identificador.
"""
from __future__ import annotations

from shared.types import ChromebooksId

from domain.repositories import ChromebookRepository

from .dtos import ChromebookOutput
from .exceptions import ChromebookNaoEncontradoError


class BuscarChromebookPorIdUseCase:
    """
    Retorna os dados de um registro de Chromebook a partir do seu
    identificador.
    """

    def __init__(self, repositorio: ChromebookRepository) -> None:
        self._repositorio = repositorio

    def executar(self, chromebook_id: ChromebooksId) -> ChromebookOutput:
        chromebook = self._repositorio.buscar_por_id(chromebook_id)

        if chromebook is None:
            raise ChromebookNaoEncontradoError(chromebook_id)

        return ChromebookOutput.de_entidade(chromebook)
