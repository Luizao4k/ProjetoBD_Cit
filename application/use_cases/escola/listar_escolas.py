"""
Caso de uso: listar todas as Escolas cadastradas.
"""
from __future__ import annotations

from domain.repositories import EscolaRepository

from .dtos import EscolaOutput


class ListarEscolasUseCase:
    """
    Retorna todas as Escolas cadastradas, prontas para
    consulta ou exportação em planilha.
    """

    def __init__(self, repositorio: EscolaRepository) -> None:
        self._repositorio = repositorio

    def executar(self) -> list[EscolaOutput]:
        escolas = self._repositorio.listar_todas()
        return [EscolaOutput.de_entidade(escola) for escola in escolas]
