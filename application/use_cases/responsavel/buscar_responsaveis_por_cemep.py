"""
Caso de uso: listar os Responsáveis de um Cemep (relação 1:N).
"""
from __future__ import annotations

from shared.types import CemepId

from domain.repositories import ResponsavelRepository

from .dtos import ResponsavelOutput


class BuscarResponsaveisPorCemepUseCase:
    """
    Retorna todos os Responsáveis vinculados a um Cemep.
    """

    def __init__(self, repositorio: ResponsavelRepository) -> None:
        self._repositorio = repositorio

    def executar(self, cemep_id: CemepId) -> list[ResponsavelOutput]:
        responsaveis = self._repositorio.buscar_por_cemep(cemep_id)
        return [ResponsavelOutput.de_entidade(r) for r in responsaveis]
