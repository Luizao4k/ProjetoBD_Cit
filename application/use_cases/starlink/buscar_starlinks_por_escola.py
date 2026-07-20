"""
Caso de uso: listar as designações de Starlink de uma Escola
(relação 1:N).
"""
from __future__ import annotations

from shared.types import EscolaId

from domain.repositories import StarlinkRepository

from .dtos import StarlinkOutput


class BuscarStarlinksPorEscolaUseCase:
    """
    Retorna todas as designações de Starlink vinculadas a uma
    Escola.
    """

    def __init__(self, repositorio: StarlinkRepository) -> None:
        self._repositorio = repositorio

    def executar(self, escola_id: EscolaId) -> list[StarlinkOutput]:
        starlinks = self._repositorio.buscar_por_escola(escola_id)
        return [StarlinkOutput.de_entidade(s) for s in starlinks]
