"""
Caso de uso: criar um novo registro de Chromebook.
"""
from __future__ import annotations

from domain.entities import Chromebook
from domain.repositories import ChromebookRepository
from domain.value_objects import Quantidade

from .dtos import ChromebookOutput, CriarChromebookInput


class CriarChromebookUseCase:
    """
    Cria um novo registro de kits de Chromebook vinculado a uma
    Escola.

    Não valida aqui se a escola já possui outro registro (relação
    1:1) — essa checagem de unicidade é responsabilidade da camada
    de persistência/infraestrutura, não do caso de uso.
    """

    def __init__(self, repositorio: ChromebookRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dados: CriarChromebookInput) -> ChromebookOutput:
        chromebook = Chromebook(
            id=None,
            escola_id=dados.escola_id,
            kit_aluno=Quantidade(dados.kit_aluno) if dados.kit_aluno else None,
            kit_professor=(
                Quantidade(dados.kit_professor) if dados.kit_professor else None
            ),
        )

        chromebook_criado = self._repositorio.salvar(chromebook)

        return ChromebookOutput.de_entidade(chromebook_criado)
