"""
Caso de uso: listar as Turmas de um Responsável (relação 1:N).
"""
from __future__ import annotations

from shared.types import ResponsavelId

from domain.repositories import TurmaCemepRepository

from .dtos import TurmaCemepOutput


class BuscarTurmasPorResponsavelUseCase:
    """
    Retorna todas as Turmas vinculadas a um Responsável.
    """

    def __init__(self, repositorio: TurmaCemepRepository) -> None:
        self._repositorio = repositorio

    def executar(self, responsavel_id: ResponsavelId) -> list[TurmaCemepOutput]:
        turmas = self._repositorio.buscar_por_responsavel(responsavel_id)
        return [TurmaCemepOutput.de_entidade(t) for t in turmas]
