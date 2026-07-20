"""
Caso de uso: atualizar um registro de Chromebook existente.
"""
from __future__ import annotations

from domain.repositories import ChromebookRepository
from domain.value_objects import Quantidade

from .dtos import AtualizarChromebookInput, ChromebookOutput
from .exceptions import ChromebookNaoEncontradoError


class AtualizarChromebookUseCase:
    """
    Atualiza a quantidade de kits de um registro de Chromebook já
    existente.

    Atualização parcial: campos não informados (None) permanecem
    inalterados.
    """

    def __init__(self, repositorio: ChromebookRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dados: AtualizarChromebookInput) -> ChromebookOutput:
        chromebook = self._repositorio.buscar_por_id(dados.id)

        if chromebook is None:
            raise ChromebookNaoEncontradoError(dados.id)

        if dados.kit_aluno is not None:
            chromebook.alterar_kit_aluno(Quantidade(dados.kit_aluno))

        if dados.kit_professor is not None:
            chromebook.alterar_kit_professor(Quantidade(dados.kit_professor))

        chromebook_atualizado = self._repositorio.atualizar(chromebook)

        return ChromebookOutput.de_entidade(chromebook_atualizado)
