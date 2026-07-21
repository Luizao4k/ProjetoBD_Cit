"""
Caso de uso: atualizar um registro de Chromebook existente.
"""

from __future__ import annotations

from domain.repositories import ChromebookRepository
from domain.value_objects import Quantidade
from shared.exceptions import (
    ChromebookNaoEncontradoError,
    PersistenciaInconsistenteError,
)
from shared.types import ChromebooksId

from .dtos import AtualizarChromebookInput, ChromebookOutput


class AtualizarChromebookUseCase:
    """
    Atualiza a quantidade de kits de um registro de Chromebook.

    A atualização é parcial: campos com valor ``None`` não são
    modificados.
    """

    def __init__(self, repositorio: ChromebookRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dados: AtualizarChromebookInput) -> ChromebookOutput:
        """
        Atualiza um registro de Chromebook existente.

        Args:
            dados:
                Dados necessários para a atualização.

        Returns:
            ChromebookOutput contendo o estado atualizado.

        Raises:
            ChromebookNaoEncontradoError:
                Caso não exista um registro com o id informado.
        """

        chromebook_id = ChromebooksId(dados.id)

        chromebook = self._repositorio.buscar_por_id(chromebook_id)

        if chromebook is None:
            raise ChromebookNaoEncontradoError(chromebook_id)

        if dados.kit_aluno is not None:
            chromebook.alterar_kit_aluno(Quantidade(dados.kit_aluno))

        if dados.kit_professor is not None:
            chromebook.alterar_kit_professor(Quantidade(dados.kit_professor))

        chromebook_atualizado = self._repositorio.atualizar(chromebook)

        if chromebook_atualizado.id is None:
            raise PersistenciaInconsistenteError(
                "O repositório retornou um Chromebook sem id."
            )

        return ChromebookOutput(
            id=chromebook_atualizado.id,
            escola_id=chromebook_atualizado.escola_id,
            kit_aluno=(
                int(chromebook_atualizado.kit_aluno)
                if chromebook_atualizado.kit_aluno
                else None
            ),
            kit_professor=(
                int(chromebook_atualizado.kit_professor)
                if chromebook_atualizado.kit_professor
                else None
            ),
            criado_em=chromebook_atualizado.criado_em,
            atualizado_em=chromebook_atualizado.atualizado_em,
        )
