"""
Caso de uso: buscar um registro de Chromebook pelo identificador.
"""

from __future__ import annotations

from domain.repositories import ChromebookRepository
from shared.exceptions import (
    ChromebookNaoEncontradoError,
    PersistenciaInconsistenteError,
)
from shared.types import ChromebooksId

from .dtos import ChromebookOutput


class BuscarChromebookPorIdUseCase:
    """
    Busca um registro de Chromebook pelo seu identificador.
    """

    def __init__(self, repositorio: ChromebookRepository) -> None:
        self._repositorio = repositorio

    def executar(self, chromebook_id: int) -> ChromebookOutput:
        """
        Busca um registro de Chromebook pelo identificador.

        Args:
            chromebook_id:
                Identificador do registro.

        Returns:
            DTO contendo os dados do registro.

        Raises:
            ChromebookNaoEncontradoError:
                Caso não exista um registro com o id informado.

            PersistenciaInconsistenteError:
                Caso o repositório retorne uma entidade persistida
                em estado inconsistente.
        """

        chromebook_id = ChromebooksId(chromebook_id)

        chromebook = self._repositorio.buscar_por_id(chromebook_id)

        if chromebook is None:
            raise ChromebookNaoEncontradoError(chromebook_id)

        if chromebook.id is None:
            raise PersistenciaInconsistenteError(
                "O repositório retornou um Chromebook sem id."
            )

        return ChromebookOutput(
            id=chromebook.id,
            escola_id=chromebook.escola_id,
            kit_aluno=int(chromebook.kit_aluno) if chromebook.kit_aluno else None,
            kit_professor=(
                int(chromebook.kit_professor) if chromebook.kit_professor else None
            ),
            criado_em=chromebook.criado_em,
            atualizado_em=chromebook.atualizado_em,
        )
