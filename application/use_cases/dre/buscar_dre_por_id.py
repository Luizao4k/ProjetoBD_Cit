"""
Caso de uso: buscar uma DRE pelo identificador.
"""
from __future__ import annotations

from shared.types import DreId

from domain.repositories import DreRepository

from .dtos import DreOutput
from .exceptions import DreNaoEncontradaError


class BuscarDrePorIdUseCase:
    """
    Retorna os dados de uma DRE a partir do seu identificador.
    """

    def __init__(self, repositorio: DreRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dre_id: DreId) -> DreOutput:
        """
        Busca a DRE pelo id. Levanta DreNaoEncontradaError
        caso ela não exista.
        """
        dre = self._repositorio.buscar_por_id(dre_id)

        if dre is None:
            raise DreNaoEncontradaError(dre_id)

        return DreOutput.de_entidade(dre)
