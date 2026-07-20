"""
Caso de uso: buscar uma Escola pelo identificador.
"""
from __future__ import annotations

from shared.types import EscolaId

from domain.repositories import EscolaRepository

from .dtos import EscolaOutput
from .exceptions import EscolaNaoEncontradaError


class BuscarEscolaPorIdUseCase:
    """
    Retorna os dados de uma Escola a partir do seu identificador.
    """

    def __init__(self, repositorio: EscolaRepository) -> None:
        self._repositorio = repositorio

    def executar(self, escola_id: EscolaId) -> EscolaOutput:
        escola = self._repositorio.buscar_por_id(escola_id)

        if escola is None:
            raise EscolaNaoEncontradaError(escola_id)

        return EscolaOutput.de_entidade(escola)
