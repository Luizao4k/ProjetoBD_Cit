"""
Caso de uso: criar uma nova DRE.
"""
from __future__ import annotations

from domain.entities import Dre
from domain.repositories import DreRepository
from domain.value_objects import Nome, Telefone

from .dtos import CriarDreInput, DreOutput


class CriarDreUseCase:
    """
    Cria uma nova DRE a partir dos dados informados.
    """

    def __init__(self, repositorio: DreRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dados: CriarDreInput) -> DreOutput:
        """
        Valida os dados (via Value Objects), persiste a nova DRE
        e retorna o DTO de saída já com o identificador gerado.
        """
        dre = Dre(
            id=None,
            nome=Nome(dados.nome),
            telefone=Telefone(dados.telefone) if dados.telefone else None,
        )

        dre_criada = self._repositorio.salvar(dre)

        return DreOutput.de_entidade(dre_criada)
