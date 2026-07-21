"""
Caso de uso: listar todos os registros de Chromebook cadastrados.
"""

from __future__ import annotations

from domain.repositories import ChromebookRepository
from shared.exceptions import PersistenciaInconsistenteError

from .dtos import ChromebookOutput


class ListarChromebooksUseCase:
    """
    Lista todos os registros de Chromebook cadastrados.
    """

    def __init__(self, repositorio: ChromebookRepository) -> None:
        self._repositorio = repositorio

    def executar(self) -> list[ChromebookOutput]:
        """
        Lista todos os registros de Chromebook cadastrados.

        Returns:
            Lista de DTOs representando os registros cadastrados.

        Raises:
            PersistenciaInconsistenteError:
                Caso o repositório retorne uma entidade persistida
                em estado inconsistente.
        """

        chromebooks = self._repositorio.listar_todas()

        resultado: list[ChromebookOutput] = []

        for chromebook in chromebooks:
            if chromebook.id is None:
                raise PersistenciaInconsistenteError(
                    "O repositório retornou um Chromebook sem id."
                )

            resultado.append(
                ChromebookOutput(
                    id=chromebook.id,
                    escola_id=chromebook.escola_id,
                    kit_aluno=int(chromebook.kit_aluno) if chromebook.kit_aluno else None,
                    kit_professor=(
                        int(chromebook.kit_professor)
                        if chromebook.kit_professor
                        else None
                    ),
                    criado_em=chromebook.criado_em,
                    atualizado_em=chromebook.atualizado_em,
                )
            )

        return resultado
