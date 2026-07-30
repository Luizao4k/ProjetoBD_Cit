"""
Caso de uso: criar um novo Responsável.
"""

from __future__ import annotations

from domain.entities import Responsavel
from domain.repositories import ResponsavelRepository
from domain.value_objects import Nome
from shared.exceptions import PersistenciaInconsistenteError
from shared.types import CemepId

from .dtos import CriarResponsavelInput, ResponsavelOutput


class CriarResponsavelUseCase:
    """
    Cria um novo Responsável vinculado a um Cemep.
    """

    def __init__(self, repositorio: ResponsavelRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dados: CriarResponsavelInput) -> ResponsavelOutput:
        """
        Cria um novo Responsável.

        Args:
            dados:
                Dados necessários para a criação do Responsável.

        Returns:
            DTO contendo os dados do Responsável criado.

        Raises:
            PersistenciaInconsistenteError:
                Caso o repositório retorne uma entidade persistida
                em estado inconsistente.
        """

        responsavel = Responsavel(
            id=None,
            cemep_id=CemepId(dados.cemep_id),
            nome=Nome(dados.nome),
        )

        responsavel_criado = self._repositorio.salvar(responsavel)

        if responsavel_criado.id is None:
            raise PersistenciaInconsistenteError(
                "O repositório retornou um Responsavel sem id."
            )

        return ResponsavelOutput(
            id=responsavel_criado.id,
            cemep_id=responsavel_criado.cemep_id,
            nome=responsavel_criado.nome.valor,
            criado_em=responsavel_criado.criado_em,
            atualizado_em=responsavel_criado.atualizado_em,
        )
