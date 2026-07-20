"""
Caso de uso: atualizar um Responsável existente.
"""
from __future__ import annotations

from domain.repositories import ResponsavelRepository
from domain.value_objects import Nome

from .dtos import AtualizarResponsavelInput, ResponsavelOutput
from .exceptions import ResponsavelNaoEncontradoError


class AtualizarResponsavelUseCase:
    """
    Atualiza os dados de um Responsável já existente.

    Atualização parcial: campos não informados (None) permanecem
    inalterados.
    """

    def __init__(self, repositorio: ResponsavelRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dados: AtualizarResponsavelInput) -> ResponsavelOutput:
        responsavel = self._repositorio.buscar_por_id(dados.id)

        if responsavel is None:
            raise ResponsavelNaoEncontradoError(dados.id)

        if dados.nome is not None:
            responsavel.alterar_nome(Nome(dados.nome))

        responsavel_atualizado = self._repositorio.atualizar(responsavel)

        return ResponsavelOutput.de_entidade(responsavel_atualizado)
