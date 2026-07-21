"""
Caso de uso: remover uma DRE existente.
"""

from __future__ import annotations

from domain.repositories import DreRepository
from shared.exceptions import DreNaoEncontradaError
from shared.types import DreId


class RemoverDreUseCase:
    """
    Remove uma DRE existente.

    Caso o identificador informado não corresponda a uma DRE
    cadastrada, uma exceção é lançada.
    """

    def __init__(self, repositorio: DreRepository) -> None:
        """
        Inicializa o caso de uso.

        Args:
            repositorio:
                Repositório responsável pela persistência das DREs.
        """
        self._repositorio = repositorio

    def executar(self, dre_id: int) -> None:
        """
        Remove uma DRE.

        Args:
            dre_id:
                Identificador da DRE.

        Raises:
            DreNaoEncontradaError:
                Caso não exista uma DRE com o identificador informado.
        """

        dre_id = DreId(dre_id)

        dre = self._repositorio.buscar_por_id(dre_id)

        if dre is None:
            raise DreNaoEncontradaError(dre_id)

        self._repositorio.remover(dre_id)
