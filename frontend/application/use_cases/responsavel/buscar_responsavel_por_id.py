"""
Caso de uso: buscar um Responsável pelo identificador.
"""

from __future__ import annotations

from domain.repositories import ResponsavelRepository
from shared.exceptions import (
    PersistenciaInconsistenteError,
    ResponsavelNaoEncontradoError,
)
from shared.types import ResponsavelId

from .dtos import ResponsavelOutput


class BuscarResponsavelPorIdUseCase:
    """
    Busca um Responsável pelo seu identificador.
    """

    def __init__(self, repositorio: ResponsavelRepository) -> None:
        self._repositorio = repositorio

    def executar(self, responsavel_id: int) -> ResponsavelOutput:
        """
        Busca um Responsável pelo identificador.

        Args:
            responsavel_id:
                Identificador do Responsável.

        Returns:
            DTO contendo os dados do Responsável.

        Raises:
            ResponsavelNaoEncontradoError:
                Caso não exista um Responsável com o id informado.

            PersistenciaInconsistenteError:
                Caso o repositório retorne uma entidade persistida
                em estado inconsistente.
        """

        responsavel_id = ResponsavelId(responsavel_id)

        responsavel = self._repositorio.buscar_por_id(responsavel_id)

        if responsavel is None:
            raise ResponsavelNaoEncontradoError(responsavel_id)

        if responsavel.id is None:
            raise PersistenciaInconsistenteError(
                "O repositório retornou um Responsavel sem id."
            )

        return ResponsavelOutput(
            id=responsavel.id,
            cemep_id=responsavel.cemep_id,
            nome=responsavel.nome.valor,
            criado_em=responsavel.criado_em,
            atualizado_em=responsavel.atualizado_em,
        )
