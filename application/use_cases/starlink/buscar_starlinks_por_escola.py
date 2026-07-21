"""
Caso de uso: listar as designações de Starlink de uma Escola
(relação 1:N).
"""

from __future__ import annotations

from domain.repositories import StarlinkRepository
from shared.exceptions import PersistenciaInconsistenteError
from shared.types import EscolaId

from .dtos import StarlinkOutput


class BuscarStarlinksPorEscolaUseCase:
    """
    Retorna todas as designações de Starlink vinculadas a uma
    Escola.

    Como se trata de uma relação 1:N, uma lista vazia é um
    resultado legítimo — não há exceção equivalente à das
    relações 1:1.
    """

    def __init__(self, repositorio: StarlinkRepository) -> None:
        self._repositorio = repositorio

    def executar(self, escola_id: int) -> list[StarlinkOutput]:
        """
        Lista as designações de Starlink de uma Escola.

        Args:
            escola_id:
                Identificador da Escola.

        Returns:
            Lista de DTOs representando as designações da escola.
            Pode ser vazia.

        Raises:
            PersistenciaInconsistenteError:
                Caso o repositório retorne uma entidade persistida
                em estado inconsistente.
        """

        id_escola = EscolaId(escola_id)

        starlinks = self._repositorio.buscar_por_escola(id_escola)

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
