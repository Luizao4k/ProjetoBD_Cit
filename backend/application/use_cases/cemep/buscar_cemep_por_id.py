"""
Caso de uso: buscar um Cemep pelo identificador.
"""

from __future__ import annotations

from domain.repositories import CemepRepository
from shared.exceptions import (
    CemepNaoEncontradoError,
    PersistenciaInconsistenteError,
)
from shared.types import CemepId

from .dtos import CemepOutput


class BuscarCemepPorIdUseCase:
    """
    Busca um Cemep pelo seu identificador.
    """

    def __init__(self, repositorio: CemepRepository) -> None:
        """
        Inicializa o caso de uso.

        Args:
            repositorio:
                Repositório responsável pela persistência dos Cemep.
        """
        self._repositorio = repositorio

    def executar(self, cemep_id: int) -> CemepOutput:
        """
        Busca um Cemep pelo identificador.

        Args:
            cemep_id:
                Identificador do Cemep.

        Returns:
            DTO contendo os dados do Cemep.

        Raises:
            CemepNaoEncontradoError:
                Caso não exista um Cemep com o id informado.

            PersistenciaInconsistenteError:
                Caso o repositório retorne uma entidade persistida
                em estado inconsistente.
        """

        cemep_id = CemepId(cemep_id)

        cemep = self._repositorio.buscar_por_id(cemep_id)

        if cemep is None:
            raise CemepNaoEncontradoError(cemep_id)

        if cemep.id is None:
            raise PersistenciaInconsistenteError(
                "O repositório retornou um Cemep sem id."
            )

        return CemepOutput(
            id=cemep.id,
            escola_id=cemep.escola_id,
            comentario=cemep.comentario.valor if cemep.comentario else None,
            criado_em=cemep.criado_em,
            atualizado_em=cemep.atualizado_em,
        )
