"""
Caso de uso: listar todos os Responsáveis cadastrados.
"""
from __future__ import annotations

from domain.repositories import ResponsavelRepository

from .dtos import ResponsavelOutput


class ListarResponsaveisUseCase:
    """
    Retorna todos os Responsáveis cadastrados, prontos para
    consulta ou exportação em planilha.
    """

    def __init__(self, repositorio: ResponsavelRepository) -> None:
        self._repositorio = repositorio

    def executar(self) -> list[ResponsavelOutput]:
        responsaveis = self._repositorio.listar_todas()
        return [ResponsavelOutput.de_entidade(r) for r in responsaveis]
