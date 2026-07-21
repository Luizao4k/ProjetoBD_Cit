"""
Caso de uso: remover um Diretor existente.
"""

from __future__ import annotations

from domain.repositories import DiretorRepository
from shared.exceptions import DiretorNaoEncontradoError
from shared.types import DiretorId


class RemoverDiretorUseCase:
    """
    Remove um Diretor existente.
    """

    def __init__(self, repositorio: DiretorRepository) -> None:
        self._repositorio = repositorio

    def executar(self, diretor_id: int) -> None:
        """
        Remove um Diretor.

        Args:
            diretor_id:
                Identificador do Diretor.

        Raises:
            DiretorNaoEncontradoError:
                Caso não exista um Diretor com o identificador informado.
        """

        diretor_id = DiretorId(diretor_id)

        diretor = self._repositorio.buscar_por_id(diretor_id)

        if diretor is None:
            raise DiretorNaoEncontradoError(diretor_id)

        self._repositorio.remover(diretor_id)
