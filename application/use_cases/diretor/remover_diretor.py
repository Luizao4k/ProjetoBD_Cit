"""
Caso de uso: remover um Diretor existente.
"""
from __future__ import annotations

from shared.types import DiretorId

from domain.repositories import DiretorRepository

from .exceptions import DiretorNaoEncontradoError


class RemoverDiretorUseCase:
    """
    Remove um Diretor existente pelo identificador.
    """

    def __init__(self, repositorio: DiretorRepository) -> None:
        self._repositorio = repositorio

    def executar(self, diretor_id: DiretorId) -> None:
        diretor = self._repositorio.buscar_por_id(diretor_id)

        if diretor is None:
            raise DiretorNaoEncontradoError(diretor_id)

        self._repositorio.remover(diretor_id)
