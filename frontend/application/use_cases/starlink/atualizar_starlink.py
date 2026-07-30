"""
Caso de uso: atualizar uma designação de Starlink existente.
"""

from __future__ import annotations

from domain.repositories import StarlinkRepository
from domain.value_objects import Nome
from shared.exceptions import (
    PersistenciaInconsistenteError,
    StarlinkNaoEncontradoError,
)
from shared.types import StarlinkId

from .dtos import AtualizarStarlinkInput, StarlinkOutput


class AtualizarStarlinkUseCase:
    """
    Atualiza uma designação de Starlink existente.

    A atualização é parcial: campos com valor ``None`` não são
    modificados.
    """

    def __init__(self, repositorio: StarlinkRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dados: AtualizarStarlinkInput) -> StarlinkOutput:
        """
        Atualiza uma designação de Starlink existente.

        Args:
            dados:
                Dados necessários para a atualização.

        Returns:
            StarlinkOutput contendo o estado atualizado.

        Raises:
            StarlinkNaoEncontradoError:
                Caso não exista uma designação com o id informado.
        """

        starlink_id = StarlinkId(dados.id)

        starlink = self._repositorio.buscar_por_id(starlink_id)

        if starlink is None:
            raise StarlinkNaoEncontradoError(starlink_id)

        if dados.designacao is not None:
            starlink.alterar_designacao(Nome(dados.designacao))

        starlink_atualizado = self._repositorio.atualizar(starlink)

        if starlink_atualizado.id is None:
            raise PersistenciaInconsistenteError(
                "O repositório retornou um Starlink sem id."
            )

        return StarlinkOutput(
            id=starlink_atualizado.id,
            escola_id=starlink_atualizado.escola_id,
            designacao=starlink_atualizado.designacao.valor,
            criado_em=starlink_atualizado.criado_em,
            atualizado_em=starlink_atualizado.atualizado_em,
        )
