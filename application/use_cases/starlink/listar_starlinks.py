"""
Caso de uso: listar todas as designações de Starlink cadastradas.
"""
from __future__ import annotations

from domain.repositories import StarlinkRepository

from .dtos import StarlinkOutput


class ListarStarlinksUseCase:
    """
    Retorna todas as designações de Starlink cadastradas, prontas
    para consulta ou exportação em planilha.
    """

    def __init__(self, repositorio: StarlinkRepository) -> None:
        self._repositorio = repositorio

    def executar(self) -> list[StarlinkOutput]:
        starlinks = self._repositorio.listar_todas()
        return [StarlinkOutput.de_entidade(s) for s in starlinks]
