"""
Caso de uso: listar todas as Turmas do Cemep cadastradas.
"""
from __future__ import annotations

from domain.repositories import TurmaCemepRepository

from .dtos import TurmaCemepOutput


class ListarTurmasCemepUseCase:
    """
    Retorna todas as Turmas cadastradas, prontas para consulta
    ou exportação em planilha.
    """

    def __init__(self, repositorio: TurmaCemepRepository) -> None:
        self._repositorio = repositorio

    def executar(self) -> list[TurmaCemepOutput]:
        turmas = self._repositorio.listar_todas()
        return [TurmaCemepOutput.de_entidade(t) for t in turmas]
