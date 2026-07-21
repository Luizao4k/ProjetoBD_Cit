"""
Caso de uso: buscar uma Escola pelo identificador.
"""

from __future__ import annotations

from domain.repositories import EscolaRepository
from shared.exceptions import (
    EscolaNaoEncontradaError,
    PersistenciaInconsistenteError,
)
from shared.types import EscolaId

from .dtos import EscolaOutput


class BuscarEscolaPorIdUseCase:
    """
    Busca uma Escola pelo seu identificador.
    """

    def __init__(self, repositorio: EscolaRepository) -> None:
        self._repositorio = repositorio

    def executar(self, escola_id: int) -> EscolaOutput:
        """
        Busca uma Escola pelo identificador.

        Args:
            escola_id:
                Identificador da Escola.

        Returns:
            DTO contendo os dados da Escola.

        Raises:
            EscolaNaoEncontradaError:
                Caso não exista uma Escola com o id informado.

            PersistenciaInconsistenteError:
                Caso o repositório retorne uma entidade persistida
                em estado inconsistente.
        """

        escola_id = EscolaId(escola_id)

        escola = self._repositorio.buscar_por_id(escola_id)

        if escola is None:
            raise EscolaNaoEncontradaError(escola_id)

        if escola.id is None:
            raise PersistenciaInconsistenteError(
                "O repositório retornou uma Escola sem id."
            )

        return EscolaOutput(
            id=escola.id,
            inep=escola.inep.valor,
            nome=escola.nome.valor,
            tipo=escola.tipo.value,
            municipio=escola.municipio.valor,
            dre_id=escola.dre_id,
            endereco=escola.endereco.valor if escola.endereco else None,
            criado_em=escola.criado_em,
            atualizado_em=escola.atualizado_em,
        )
