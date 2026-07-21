"""
Caso de uso: remover uma Escola existente.
"""

from __future__ import annotations

from domain.repositories import EscolaRepository
from shared.exceptions import EscolaNaoEncontradaError
from shared.types import EscolaId


class RemoverEscolaUseCase:
    """
    Remove uma Escola existente.
    """

    def __init__(self, repositorio: EscolaRepository) -> None:
        self._repositorio = repositorio

    def executar(self, escola_id: int) -> None:
        """
        Remove uma Escola.

        Args:
            escola_id:
                Identificador da Escola.

        Raises:
            EscolaNaoEncontradaError:
                Caso não exista uma Escola com o identificador
                informado.
        """

        escola_id = EscolaId(escola_id)

        escola = self._repositorio.buscar_por_id(escola_id)

        if escola is None:
            raise EscolaNaoEncontradaError(escola_id)

        self._repositorio.remover(escola_id)
