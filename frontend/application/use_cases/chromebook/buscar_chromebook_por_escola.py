"""
Caso de uso: buscar o registro de Chromebook de uma Escola
(relação 1:1).
"""

from __future__ import annotations

from domain.repositories import ChromebookRepository
from shared.exceptions import (
    EscolaNaoPossuiChromebookError,
    PersistenciaInconsistenteError,
)
from shared.types import EscolaId

from .dtos import ChromebookOutput


class BuscarChromebookPorEscolaUseCase:
    """
    Retorna o registro de Chromebook vinculado à escola informada.

    Raises:
        EscolaNaoPossuiChromebookError:
            Caso a escola não possua registro de Chromebook.
    """

    def __init__(self, repositorio: ChromebookRepository) -> None:
        self._repositorio = repositorio

    def executar(self, escola_id: int) -> ChromebookOutput:
        """
        Busca o registro de Chromebook associado à escola informada.

        Args:
            escola_id:
                Identificador da escola.

        Returns:
            DTO contendo os dados do registro.

        Raises:
            EscolaNaoPossuiChromebookError:
                Caso não exista um registro vinculado à escola.
        """

        id_escola = EscolaId(escola_id)

        chromebook = self._repositorio.buscar_por_escola(id_escola)

        if chromebook is None:
            raise EscolaNaoPossuiChromebookError(id_escola)

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
