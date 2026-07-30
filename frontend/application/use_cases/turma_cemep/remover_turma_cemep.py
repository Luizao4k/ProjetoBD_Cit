"""
Caso de uso: remover uma Turma do Cemep existente.
"""

from __future__ import annotations

from domain.repositories import TurmaCemepRepository
from shared.exceptions import TurmaCemepNaoEncontradaError
from shared.types import TurmaCemepId


class RemoverTurmaCemepUseCase:
    """
    Remove uma Turma existente.
    """

    def __init__(self, repositorio: TurmaCemepRepository) -> None:
        self._repositorio = repositorio

    def executar(self, turma_id: int) -> None:
        """
        Remove uma Turma.

        Args:
            turma_id:
                Identificador da Turma.

        Raises:
            TurmaCemepNaoEncontradaError:
                Caso não exista uma Turma com o identificador
                informado.
        """

        turma_id = TurmaCemepId(turma_id)

        turma = self._repositorio.buscar_por_id(turma_id)

        if turma is None:
            raise TurmaCemepNaoEncontradaError(turma_id)

        self._repositorio.remover(turma_id)
