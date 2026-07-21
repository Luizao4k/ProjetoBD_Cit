"""
Caso de uso: buscar uma designação de Starlink pelo identificador.
"""

from __future__ import annotations

from domain.repositories import StarlinkRepository
from shared.exceptions import (
    PersistenciaInconsistenteError,
    StarlinkNaoEncontradoError,
)
from shared.types import StarlinkId

from .dtos import StarlinkOutput


class BuscarStarlinkPorIdUseCase:
    """
    Busca uma designação de Starlink pelo seu identificador.
    """

    def __init__(self, repositorio: StarlinkRepository) -> None:
        self._repositorio = repositorio

    def executar(self, starlink_id: int) -> StarlinkOutput:
        """
        Busca uma designação de Starlink pelo identificador.

        Args:
            starlink_id:
                Identificador da designação.

        Returns:
            DTO contendo os dados da designação.

        Raises:
            StarlinkNaoEncontradoError:
                Caso não exista uma designação com o id informado.

            PersistenciaInconsistenteError:
                Caso o repositório retorne uma entidade persistida
                em estado inconsistente.
        """

        starlink_id = StarlinkId(starlink_id)

        starlink = self._repositorio.buscar_por_id(starlink_id)

        if starlink is None:
            raise StarlinkNaoEncontradoError(starlink_id)

        if starlink.id is None:
            raise PersistenciaInconsistenteError(
                "O repositório retornou um Starlink sem id."
            )

        return StarlinkOutput(
            id=starlink.id,
            escola_id=starlink.escola_id,
            designacao=starlink.designacao.valor,
            criado_em=starlink.criado_em,
            atualizado_em=starlink.atualizado_em,
        )
