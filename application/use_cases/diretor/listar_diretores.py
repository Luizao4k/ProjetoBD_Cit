"""
Caso de uso: listar todos os Diretores cadastrados.
"""
from __future__ import annotations

from domain.repositories import DiretorRepository

from .dtos import DiretorOutput


class ListarDiretoresUseCase:
    """
    Retorna todos os Diretores cadastrados, prontos para
    consulta ou exportação em planilha.
    """

    def __init__(self, repositorio: DiretorRepository) -> None:
        self._repositorio = repositorio

    def executar(self) -> list[DiretorOutput]:
        diretores = self._repositorio.listar_todas()
        return [DiretorOutput.de_entidade(diretor) for diretor in diretores]
