"""
Caso de uso: listar todas as designações de Starlink cadastradas.
"""

from __future__ import annotations

from domain.repositories import StarlinkRepository
from shared.exceptions import PersistenciaInconsistenteError

from .dtos import StarlinkOutput


class ListarStarlinksUseCase:
    """
    Lista todas as designações de Starlink cadastradas.
    """

    def __init__(self, repositorio: StarlinkRepository) -> None:
        self._repositorio = repositorio

    def executar(self) -> list[StarlinkOutput]:
        """
        Lista todas as designações de Starlink cadastradas.

        Returns:
            Lista de DTOs representando as designações cadastradas.

        Raises:
            PersistenciaInconsistenteError:
                Caso o repositório retorne uma entidade persistida
                em estado inconsistente.
        """

        starlinks = self._repositorio.listar_todas()

        resultado: list[StarlinkOutput] = []

        for starlink in starlinks:
            if starlink.id is None:
                raise PersistenciaInconsistenteError(
                    "O repositório retornou um Starlink sem id."
                )

            resultado.append(
                StarlinkOutput(
                    id=starlink.id,
                    escola_id=starlink.escola_id,
                    designacao=starlink.designacao.valor,
                    criado_em=starlink.criado_em,
                    atualizado_em=starlink.atualizado_em,
                )
            )

        return resultado
