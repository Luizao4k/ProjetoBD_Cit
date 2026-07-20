"""
Caso de uso: listar as Escolas de uma DRE.
"""
from __future__ import annotations

from shared.types import DreId

from domain.repositories import EscolaRepository

from .dtos import EscolaOutput


class BuscarEscolasPorDreUseCase:
    """
    Retorna todas as Escolas vinculadas a uma DRE — útil tanto
    para consulta quanto para exportação de planilha por regional.
    """

    def __init__(self, repositorio: EscolaRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dre_id: DreId) -> list[EscolaOutput]:
        escolas = self._repositorio.buscar_por_dre(dre_id)
        return [EscolaOutput.de_entidade(escola) for escola in escolas]
