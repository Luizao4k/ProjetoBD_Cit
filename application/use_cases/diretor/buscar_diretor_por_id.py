"""
Caso de uso: buscar um Diretor pelo identificador.
"""
from __future__ import annotations

from shared.types import DiretorId

from domain.repositories import DiretorRepository

from .dtos import DiretorOutput
from .exceptions import DiretorNaoEncontradoError


class BuscarDiretorPorIdUseCase:
    """
    Retorna os dados de um Diretor a partir do seu identificador.
    """

    def __init__(self, repositorio: DiretorRepository) -> None:
        self._repositorio = repositorio

    def executar(self, diretor_id: DiretorId) -> DiretorOutput:
        diretor = self._repositorio.buscar_por_id(diretor_id)

        if diretor is None:
            raise DiretorNaoEncontradoError(diretor_id)

        return DiretorOutput.de_entidade(diretor)
