"""
Caso de uso: criar uma nova designação de Starlink.
"""

from __future__ import annotations

from domain.entities import Starlink
from domain.repositories import StarlinkRepository
from domain.value_objects import Nome
from shared.exceptions import PersistenciaInconsistenteError, DesignacaoStarlinkDuplicadaError
from shared.types import EscolaId

from .dtos import CriarStarlinkInput, StarlinkOutput


class CriarStarlinkUseCase:
    """
    Cria uma nova designação de Starlink vinculada a uma Escola.

    Uma escola pode ter mais de uma designação (relação 1:N).
    """

    def __init__(self, repositorio: StarlinkRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dados: CriarStarlinkInput) -> StarlinkOutput:
        """
        Cria uma nova designação de Starlink.

        Args:
            dados:
                Dados necessários para a criação.

        Returns:
            DTO contendo os dados da designação criada.

        Raises:
            PersistenciaInconsistenteError:
                Caso o repositório retorne uma entidade persistida
                em estado inconsistente.
        """
        designacao_existente = (
                self._repositorio.buscar_por_designacao(
                    dados.designacao
                )
            )

        if designacao_existente is not None:
            raise DesignacaoStarlinkDuplicadaError(
                f"A designação '{dados.designacao}' já está cadastrada."
            )
        
        starlink = Starlink(
            id=None,
            escola_id=EscolaId(dados.escola_id),
            designacao=Nome(dados.designacao),
        )

        starlink_criado = self._repositorio.salvar(starlink)

        if starlink_criado.id is None:
            raise PersistenciaInconsistenteError(
                "O repositório retornou um Starlink sem id."
            )

        return StarlinkOutput(
            id=starlink_criado.id,
            escola_id=starlink_criado.escola_id,
            designacao=starlink_criado.designacao.valor,
            criado_em=starlink_criado.criado_em,
            atualizado_em=starlink_criado.atualizado_em,
        )
