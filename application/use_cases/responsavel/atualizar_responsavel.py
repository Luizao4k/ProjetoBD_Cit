"""
Caso de uso: atualizar um Responsável existente.
"""

from __future__ import annotations

from domain.repositories import ResponsavelRepository
from domain.value_objects import Nome
from shared.exceptions import (
    PersistenciaInconsistenteError,
    ResponsavelNaoEncontradoError,
)
from shared.types import ResponsavelId

from .dtos import AtualizarResponsavelInput, ResponsavelOutput


class AtualizarResponsavelUseCase:
    """
    Atualiza um Responsável existente.

    A atualização é parcial: campos com valor ``None`` não são
    modificados.
    """

    def __init__(self, repositorio: ResponsavelRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dados: AtualizarResponsavelInput) -> ResponsavelOutput:
        """
        Atualiza um Responsável existente.

        Args:
            dados:
                Dados necessários para a atualização.

        Returns:
            ResponsavelOutput contendo o estado atualizado.

        Raises:
            ResponsavelNaoEncontradoError:
                Caso não exista um Responsável com o id informado.
        """

        responsavel_id = ResponsavelId(dados.id)

        responsavel = self._repositorio.buscar_por_id(responsavel_id)

        if responsavel is None:
            raise ResponsavelNaoEncontradoError(responsavel_id)

        if dados.nome is not None:
            responsavel.alterar_nome(Nome(dados.nome))

        responsavel_atualizado = self._repositorio.atualizar(responsavel)

        if responsavel_atualizado.id is None:
            raise PersistenciaInconsistenteError(
                "O repositório retornou um Responsavel sem id."
            )

        return ResponsavelOutput(
            id=responsavel_atualizado.id,
            cemep_id=responsavel_atualizado.cemep_id,
            nome=responsavel_atualizado.nome.valor,
            criado_em=responsavel_atualizado.criado_em,
            atualizado_em=responsavel_atualizado.atualizado_em,
        )
