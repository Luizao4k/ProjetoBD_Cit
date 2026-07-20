"""
Caso de uso: buscar uma Turma do Cemep pelo identificador.
"""
from __future__ import annotations

from shared.types import TurmaCemepId

from domain.repositories import TurmaCemepRepository

from .dtos import TurmaCemepOutput
from .exceptions import TurmaCemepNaoEncontradaError


class BuscarTurmaCemepPorIdUseCase:
    """
    Retorna os dados de uma Turma a partir do seu identificador.
    """

    def __init__(self, repositorio: TurmaCemepRepository) -> None:
        self._repositorio = repositorio

    def executar(self, turma_id: TurmaCemepId) -> TurmaCemepOutput:
        turma = self._repositorio.buscar_por_id(turma_id)

        if turma is None:
            raise TurmaCemepNaoEncontradaError(turma_id)

        return TurmaCemepOutput.de_entidade(turma)
