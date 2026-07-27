"""
Caso de uso: listar todos os Cemeps cadastrados.
"""

from __future__ import annotations

from domain.repositories import CemepRepository
from shared.exceptions import PersistenciaInconsistenteError

from .dtos import CemepOutput


class ListarCemepsUseCase:
    """
    Lista todos os Cemeps cadastrados.

    Os dados retornados são convertidos para DTOs, ficando
    prontos para consumo por APIs, interfaces gráficas ou
    exportação.
    """

    def __init__(self, repositorio: CemepRepository) -> None:
        """
        Inicializa o caso de uso.

        Args:
            repositorio:
                Repositório responsável pela persistência dos Cemeps.
        """
        self._repositorio = repositorio

    def executar(self) -> list[CemepOutput]:
        """
        Lista todos os Cemeps cadastrados.

        Returns:
            Lista de DTOs representando os Cemeps cadastrados.

        Raises:
            PersistenciaInconsistenteError:
                Caso o repositório retorne uma entidade persistida
                em estado inconsistente.
        """

        cemeps = self._repositorio.listar_todas()

        resultado: list[CemepOutput] = []

        for cemep in cemeps:
            if cemep.id is None:
                raise PersistenciaInconsistenteError(
                    "O repositório retornou um Cemep sem id."
                )

            resultado.append(
                CemepOutput(
                    id=cemep.id,
                    escola_id=cemep.escola_id,
                    comentario=cemep.comentario.valor if cemep.comentario else None,
                    criado_em=cemep.criado_em,
                    atualizado_em=cemep.atualizado_em,
                )
            )

        return resultado
