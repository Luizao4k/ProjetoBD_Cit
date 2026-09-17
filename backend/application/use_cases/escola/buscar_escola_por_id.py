"""
Caso de uso: buscar uma Escola pelo identificador.
"""

from __future__ import annotations


from domain.repositories import EscolaRepository, DreRepository
from shared.exceptions import (
    EscolaNaoEncontradaError,
    PersistenciaInconsistenteError,
    DreNaoEncontradaError,
)
from shared.types import EscolaId

from .dtos import EscolaOutput
from ..dre.dtos import DreOutput


class BuscarEscolaPorIdUseCase:
    """
    Busca uma Escola pelo seu identificador.
    """

    def __init__(self, repositorio: EscolaRepository, dre_repositorio: DreRepository) -> None:
        self._repositorio = repositorio
        self._dre_repositorio = dre_repositorio

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

        dre_output = None
        if escola.dre_id:
            dre = self._dre_repositorio.buscar_por_id(escola.dre_id)
            if dre is None:
                raise DreNaoEncontradaError(escola.dre_id)

            if dre.id is None:
                raise PersistenciaInconsistenteError(
                    "O repositório retornou uma DRE sem id."
                )

            # Monta o DTO da DRE
            dre_output = DreOutput(
                id=dre.id,
                nome=dre.nome.valor,
                telefone=dre.telefone.valor if dre.telefone else None,
                criado_em=dre.criado_em,
                atualizado_em=dre.atualizado_em,
            )

        return EscolaOutput(
            id=escola.id,
            inep=escola.inep.valor,
            nome=escola.nome.valor,
            tipo=escola.tipo.value,
            municipio=escola.municipio.valor,
            dre_id=escola.dre_id,
            dre=dre_output,
            endereco=escola.endereco.valor if escola.endereco else None,
            criado_em=escola.criado_em,
            atualizado_em=escola.atualizado_em,
        )
