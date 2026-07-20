"""
Caso de uso: buscar o Diretor de uma Escola (relação 1:1).
"""
from __future__ import annotations

from shared.types import EscolaId

from domain.repositories import DiretorRepository

from .dtos import DiretorOutput


class BuscarDiretorPorEscolaUseCase:
    """
    Retorna o Diretor vinculado à escola informada, ou None
    caso a escola ainda não tenha diretor definido.
    """

    def __init__(self, repositorio: DiretorRepository) -> None:
        self._repositorio = repositorio

    def executar(self, escola_id: EscolaId) -> DiretorOutput | None:
        diretor = self._repositorio.buscar_por_escola(escola_id)

        if diretor is None:
            return None

        return DiretorOutput.de_entidade(diretor)
