"""
Caso de uso: remover uma Turma do Cemep existente.
"""
from __future__ import annotations

from shared.types import TurmaCemepId

from domain.repositories import TurmaCemepRepository

from .exceptions import TurmaCemepNaoEncontradaError


class RemoverTurmaCemepUseCase:
    """
    Remove uma Turma existente pelo identificador.
    """

    def __init__(self, repositorio: TurmaCemepRepository) -> None:
        self._repositorio = repositorio

    def executar(self, turma_id: TurmaCemepId) -> None:
        turma = self._repositorio.buscar_por_id(turma_id)

        if turma is None:
            raise TurmaCemepNaoEncontradaError(turma_id)

        self._repositorio.remover(turma_id)
