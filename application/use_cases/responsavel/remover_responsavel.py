"""
Caso de uso: remover um Responsável existente.
"""

from __future__ import annotations

from domain.repositories import ResponsavelRepository
from shared.exceptions import ResponsavelNaoEncontradoError
from shared.types import ResponsavelId


class RemoverResponsavelUseCase:
    """
    Remove um Responsável existente.
    """

    def __init__(self, repositorio: ResponsavelRepository) -> None:
        self._repositorio = repositorio

    def executar(self, responsavel_id: int) -> None:
        """
        Remove um Responsável.

        Args:
            responsavel_id:
                Identificador do Responsável.

        Raises:
            ResponsavelNaoEncontradoError:
                Caso não exista um Responsável com o identificador
                informado.
        """

        responsavel_id = ResponsavelId(responsavel_id)

        responsavel = self._repositorio.buscar_por_id(responsavel_id)

        if responsavel is None:
            raise ResponsavelNaoEncontradoError(responsavel_id)

        self._repositorio.remover(responsavel_id)
