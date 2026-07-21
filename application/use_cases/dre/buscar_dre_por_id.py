"""
Caso de uso: buscar uma DRE pelo identificador.
"""

from __future__ import annotations

from domain.repositories import DreRepository
from shared.exceptions import DreNaoEncontradaError, PersistenciaInconsistenteError
from shared.types import DreId

from .dtos import DreOutput


class BuscarDrePorIdUseCase:
    """
    Busca uma DRE pelo seu identificador.
    """

    def __init__(self, repositorio: DreRepository) -> None:
        """
        Inicializa o caso de uso.

        Args:
            repositorio:
                Repositório responsável pela persistência das DREs.
        """
        self._repositorio = repositorio

    def executar(self, dre_id: int) -> DreOutput:
        """
        Busca uma DRE pelo identificador.

        Args:
            dre_id:
                Identificador da DRE.

        Returns:
            DTO contendo os dados da DRE.

        Raises:
            DreNaoEncontradaError:
                Caso não exista uma DRE com o id informado.

            PersistenciaInconsistenteError:
                Caso o repositório retorne uma entidade persistida
                em estado inconsistente.
        """

        dre_id = DreId(dre_id)

        dre = self._repositorio.buscar_por_id(dre_id)

        if dre is None:
            raise DreNaoEncontradaError(dre_id)

        if dre.id is None:
            raise PersistenciaInconsistenteError(
                "O repositório retornou uma DRE sem id."
            )

        return DreOutput(
            id=dre.id,
            nome=dre.nome.valor,
            telefone=dre.telefone.valor if dre.telefone else None,
            criado_em=dre.criado_em,
            atualizado_em=dre.atualizado_em,
        )
