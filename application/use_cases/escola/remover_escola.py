"""
Caso de uso: remover uma Escola existente.
"""
from __future__ import annotations

from shared.types import EscolaId

from domain.repositories import EscolaRepository

from .exceptions import EscolaNaoEncontradaError


class RemoverEscolaUseCase:
    """
    Remove uma Escola existente pelo identificador.
    """

    def __init__(self, repositorio: EscolaRepository) -> None:
        self._repositorio = repositorio

    def executar(self, escola_id: EscolaId) -> None:
        escola = self._repositorio.buscar_por_id(escola_id)

        if escola is None:
            raise EscolaNaoEncontradaError(escola_id)

        self._repositorio.remover(escola_id)
