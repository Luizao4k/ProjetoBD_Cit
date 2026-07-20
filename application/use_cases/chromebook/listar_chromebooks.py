"""
Caso de uso: listar todos os registros de Chromebook cadastrados.
"""
from __future__ import annotations

from domain.repositories import ChromebookRepository

from .dtos import ChromebookOutput


class ListarChromebooksUseCase:
    """
    Retorna todos os registros de Chromebook cadastrados, prontos
    para consulta ou exportação em planilha.
    """

    def __init__(self, repositorio: ChromebookRepository) -> None:
        self._repositorio = repositorio

    def executar(self) -> list[ChromebookOutput]:
        chromebooks = self._repositorio.listar_todas()
        return [ChromebookOutput.de_entidade(c) for c in chromebooks]
