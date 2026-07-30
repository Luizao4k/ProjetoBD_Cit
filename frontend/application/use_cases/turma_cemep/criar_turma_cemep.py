"""
Caso de uso: criar uma nova Turma do Cemep.
"""

from __future__ import annotations

from domain.entities import TurmaCemep
from domain.repositories import TurmaCemepRepository
from domain.value_objects import Nome
from shared.exceptions import PersistenciaInconsistenteError
from shared.types import ResponsavelId

from .dtos import CriarTurmaCemepInput, TurmaCemepOutput


class CriarTurmaCemepUseCase:
    """
    Cria uma nova Turma vinculada a um Responsável.

    Um responsável pode ter mais de uma turma (relação 1:N).
    """

    def __init__(self, repositorio: TurmaCemepRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dados: CriarTurmaCemepInput) -> TurmaCemepOutput:
        """
        Cria uma nova Turma.

        Args:
            dados:
                Dados necessários para a criação da Turma.

        Returns:
            DTO contendo os dados da Turma criada.

        Raises:
            PersistenciaInconsistenteError:
                Caso o repositório retorne uma entidade persistida
                em estado inconsistente.
        """

        turma = TurmaCemep(
            id=None,
            responsavel_id=ResponsavelId(dados.responsavel_id),
            nome_turma=Nome(dados.nome_turma),
        )

        turma_criada = self._repositorio.salvar(turma)

        if turma_criada.id is None:
            raise PersistenciaInconsistenteError(
                "O repositório retornou uma TurmaCemep sem id."
            )

        return TurmaCemepOutput(
            id=turma_criada.id,
            responsavel_id=turma_criada.responsavel_id,
            nome_turma=turma_criada.nome_turma.valor,
            criado_em=turma_criada.criado_em,
            atualizado_em=turma_criada.atualizado_em,
        )
