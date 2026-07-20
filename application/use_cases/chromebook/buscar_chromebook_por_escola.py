"""
Caso de uso: buscar o registro de Chromebook de uma Escola
(relação 1:1).
"""
from __future__ import annotations

from shared.types import EscolaId

from domain.repositories import ChromebookRepository

from .dtos import ChromebookOutput


class BuscarChromebookPorEscolaUseCase:
    """
    Retorna o registro de Chromebook vinculado à escola informada,
    ou None caso a escola não possua registro.
    """

    def __init__(self, repositorio: ChromebookRepository) -> None:
        self._repositorio = repositorio

    def executar(self, escola_id: EscolaId) -> ChromebookOutput | None:
        chromebook = self._repositorio.buscar_por_escola(escola_id)

        if chromebook is None:
            return None

        return ChromebookOutput.de_entidade(chromebook)
