"""
Caso de uso: listar todas as DREs cadastradas.
"""
from __future__ import annotations

from domain.repositories import DreRepository

from .dtos import DreOutput


class ListarDresUseCase:
    """
    Retorna todas as DREs cadastradas, prontas para
    consulta ou exportação em planilha.
    """

    def __init__(self, repositorio: DreRepository) -> None:
        self._repositorio = repositorio

    def executar(self) -> list[DreOutput]:
        dres = self._repositorio.listar_todas()
        return [DreOutput.de_entidade(dre) for dre in dres]
