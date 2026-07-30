"""
Caso de uso: atualizar uma Turma do Cemep existente.
"""

from __future__ import annotations

from domain.repositories import TurmaCemepRepository
from domain.value_objects import Nome
from shared.exceptions import (
    PersistenciaInconsistenteError,
    TurmaCemepNaoEncontradaError,
)
from shared.types import TurmaCemepId

from .dtos import AtualizarTurmaCemepInput, TurmaCemepOutput


class AtualizarTurmaCemepUseCase:
    """
    Atualiza uma Turma existente.

    A atualização é parcial: campos com valor ``None`` não são
    modificados.
    """

    def __init__(self, repositorio: TurmaCemepRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dados: AtualizarTurmaCemepInput) -> TurmaCemepOutput:
        """
        Atualiza uma Turma existente.

        Args:
            dados:
                Dados necessários para a atualização.

        Returns:
            TurmaCemepOutput contendo o estado atualizado.

        Raises:
            TurmaCemepNaoEncontradaError:
                Caso não exista uma Turma com o id informado.
        """

        turma_id = TurmaCemepId(dados.id)

        turma = self._repositorio.buscar_por_id(turma_id)

        if turma is None:
            raise TurmaCemepNaoEncontradaError(turma_id)

        if dados.nome_turma is not None:
            turma.alterar_nome(Nome(dados.nome_turma))

        turma_atualizada = self._repositorio.atualizar(turma)

        if turma_atualizada.id is None:
            raise PersistenciaInconsistenteError(
                "O repositório retornou uma TurmaCemep sem id."
            )

        return TurmaCemepOutput(
            id=turma_atualizada.id,
            responsavel_id=turma_atualizada.responsavel_id,
            nome_turma=turma_atualizada.nome_turma.valor,
            criado_em=turma_atualizada.criado_em,
            atualizado_em=turma_atualizada.atualizado_em,
        )
