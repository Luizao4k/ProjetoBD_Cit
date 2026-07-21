"""
Caso de uso: criar um novo registro de Chromebook.
"""

from __future__ import annotations

from domain.entities import Chromebook
from domain.repositories import ChromebookRepository
from domain.value_objects import Quantidade
from shared.exceptions import PersistenciaInconsistenteError
from shared.types import EscolaId

from .dtos import ChromebookOutput, CriarChromebookInput


class CriarChromebookUseCase:
    """
    Cria um novo registro de kits de Chromebook vinculado a uma
    escola.

    A verificação de unicidade (uma escola possuir apenas um
    registro) é responsabilidade da camada de persistência.
    """

    def __init__(self, repositorio: ChromebookRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dados: CriarChromebookInput) -> ChromebookOutput:
        """
        Cria um novo registro de Chromebook.

        Args:
            dados:
                Dados necessários para a criação do registro.

        Returns:
            DTO contendo os dados do registro criado.

        Raises:
            PersistenciaInconsistenteError:
                Caso o repositório retorne uma entidade persistida
                em estado inconsistente.
        """

        chromebook = Chromebook(
            id=None,
            escola_id=EscolaId(dados.escola_id),
            kit_aluno=Quantidade(dados.kit_aluno) if dados.kit_aluno else None,
            kit_professor=(
                Quantidade(dados.kit_professor) if dados.kit_professor else None
            ),
        )

        chromebook_criado = self._repositorio.salvar(chromebook)

        if chromebook_criado.id is None:
            raise PersistenciaInconsistenteError(
                "O repositório retornou um Chromebook sem id."
            )

        return ChromebookOutput(
            id=chromebook_criado.id,
            escola_id=chromebook_criado.escola_id,
            kit_aluno=int(chromebook_criado.kit_aluno) if chromebook_criado.kit_aluno else None,
            kit_professor=(
                int(chromebook_criado.kit_professor)
                if chromebook_criado.kit_professor
                else None
            ),
            criado_em=chromebook_criado.criado_em,
            atualizado_em=chromebook_criado.atualizado_em,
        )
