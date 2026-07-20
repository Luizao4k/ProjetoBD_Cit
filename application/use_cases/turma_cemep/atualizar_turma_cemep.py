"""
Caso de uso: atualizar uma Turma do Cemep existente.
"""
from __future__ import annotations

from domain.repositories import TurmaCemepRepository
from domain.value_objects import Nome

from .dtos import AtualizarTurmaCemepInput, TurmaCemepOutput
from .exceptions import TurmaCemepNaoEncontradaError


class AtualizarTurmaCemepUseCase:
    """
    Atualiza os dados de uma Turma já existente.

    Atualização parcial: campos não informados (None) permanecem
    inalterados.
    """

    def __init__(self, repositorio: TurmaCemepRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dados: AtualizarTurmaCemepInput) -> TurmaCemepOutput:
        turma = self._repositorio.buscar_por_id(dados.id)

        if turma is None:
            raise TurmaCemepNaoEncontradaError(dados.id)

        if dados.nome_turma is not None:
            turma.alterar_nome(Nome(dados.nome_turma))

        turma_atualizada = self._repositorio.atualizar(turma)

        return TurmaCemepOutput.de_entidade(turma_atualizada)
