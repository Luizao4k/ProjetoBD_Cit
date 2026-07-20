"""
Caso de uso: atualizar uma DRE existente.
"""
from __future__ import annotations

from domain.repositories import DreRepository
from domain.value_objects import Nome, Telefone

from .dtos import AtualizarDreInput, DreOutput
from .exceptions import DreNaoEncontradaError


class AtualizarDreUseCase:
    """
    Atualiza os dados de uma DRE já existente.

    Atualização parcial: campos não informados (None) no
    AtualizarDreInput permanecem inalterados.
    """

    def __init__(self, repositorio: DreRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dados: AtualizarDreInput) -> DreOutput:
        dre = self._repositorio.buscar_por_id(dados.id)

        if dre is None:
            raise DreNaoEncontradaError(dados.id)

        if dados.nome is not None:
            dre.alterar_nome(Nome(dados.nome))

        if dados.telefone is not None:
            dre.alterar_telefone(Telefone(dados.telefone))

        dre_atualizada = self._repositorio.atualizar(dre)

        return DreOutput.de_entidade(dre_atualizada)
