"""
Caso de uso: buscar uma Turma do Cemep pelo identificador.
"""

from __future__ import annotations

from domain.repositories import TurmaCemepRepository
from shared.exceptions import (
    PersistenciaInconsistenteError,
    TurmaCemepNaoEncontradaError,
)
from shared.types import TurmaCemepId

from .dtos import TurmaCemepOutput


class BuscarTurmaCemepPorIdUseCase:
    """
    Busca uma Turma pelo seu identificador.
    """

    def __init__(self, repositorio: TurmaCemepRepository) -> None:
        self._repositorio = repositorio

    def executar(self, turma_id: int) -> TurmaCemepOutput:
        """
        Busca uma Turma pelo identificador.

        Args:
            turma_id:
                Identificador da Turma.

        Returns:
            DTO contendo os dados da Turma.

        Raises:
            TurmaCemepNaoEncontradaError:
                Caso não exista uma Turma com o id informado.

            PersistenciaInconsistenteError:
                Caso o repositório retorne uma entidade persistida
                em estado inconsistente.
        """

        turma_id = TurmaCemepId(turma_id)

        turma = self._repositorio.buscar_por_id(turma_id)

        if turma is None:
            raise TurmaCemepNaoEncontradaError(turma_id)

        if turma.id is None:
            raise PersistenciaInconsistenteError(
                "O repositório retornou uma TurmaCemep sem id."
            )

        return TurmaCemepOutput(
            id=turma.id,
            responsavel_id=turma.responsavel_id,
            nome_turma=turma.nome_turma.valor,
            criado_em=turma.criado_em,
            atualizado_em=turma.atualizado_em,
        )
