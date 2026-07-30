"""
Caso de uso: remover um registro de Chromebook existente.
"""

from __future__ import annotations

from domain.repositories import ChromebookRepository
from shared.exceptions import ChromebookNaoEncontradoError
from shared.types import ChromebooksId


class RemoverChromebookUseCase:
    """
    Remove um registro de Chromebook existente.
    """

    def __init__(self, repositorio: ChromebookRepository) -> None:
        self._repositorio = repositorio

    def executar(self, chromebook_id: int) -> None:
        """
        Remove um registro de Chromebook.

        Args:
            chromebook_id:
                Identificador do registro.

        Raises:
            ChromebookNaoEncontradoError:
                Caso não exista um registro com o identificador
                informado.
        """

        chromebook_id = ChromebooksId(chromebook_id)

        chromebook = self._repositorio.buscar_por_id(chromebook_id)

        if chromebook is None:
            raise ChromebookNaoEncontradoError(chromebook_id)

        self._repositorio.remover(chromebook_id)
