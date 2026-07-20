"""
Caso de uso: criar uma nova Turma do Cemep.
"""
from __future__ import annotations

from domain.entities import TurmaCemep
from domain.repositories import TurmaCemepRepository
from domain.value_objects import Nome

from .dtos import CriarTurmaCemepInput, TurmaCemepOutput


class CriarTurmaCemepUseCase:
    """
    Cria uma nova Turma vinculada a um Responsável.

    Um responsável pode ter mais de uma turma (relação 1:N).
    """

    def __init__(self, repositorio: TurmaCemepRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dados: CriarTurmaCemepInput) -> TurmaCemepOutput:
        turma = TurmaCemep(
            id=None,
            responsavel_id=dados.responsavel_id,
            nome_turma=Nome(dados.nome_turma),
        )

        turma_criada = self._repositorio.salvar(turma)

        return TurmaCemepOutput.de_entidade(turma_criada)
