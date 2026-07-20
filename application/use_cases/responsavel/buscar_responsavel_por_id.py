"""
Caso de uso: buscar um Responsável pelo identificador.
"""
from __future__ import annotations

from shared.types import ResponsavelId

from domain.repositories import ResponsavelRepository

from .dtos import ResponsavelOutput
from .exceptions import ResponsavelNaoEncontradoError


class BuscarResponsavelPorIdUseCase:
    """
    Retorna os dados de um Responsável a partir do seu
    identificador.
    """

    def __init__(self, repositorio: ResponsavelRepository) -> None:
        self._repositorio = repositorio

    def executar(self, responsavel_id: ResponsavelId) -> ResponsavelOutput:
        responsavel = self._repositorio.buscar_por_id(responsavel_id)

        if responsavel is None:
            raise ResponsavelNaoEncontradoError(responsavel_id)

        return ResponsavelOutput.de_entidade(responsavel)
