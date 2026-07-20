"""
Caso de uso: atualizar uma designação de Starlink existente.
"""
from __future__ import annotations

from domain.repositories import StarlinkRepository
from domain.value_objects import Nome

from .dtos import AtualizarStarlinkInput, StarlinkOutput
from .exceptions import StarlinkNaoEncontradoError


class AtualizarStarlinkUseCase:
    """
    Atualiza os dados de uma designação de Starlink já existente.

    Atualização parcial: campos não informados (None) permanecem
    inalterados.
    """

    def __init__(self, repositorio: StarlinkRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dados: AtualizarStarlinkInput) -> StarlinkOutput:
        starlink = self._repositorio.buscar_por_id(dados.id)

        if starlink is None:
            raise StarlinkNaoEncontradoError(dados.id)

        if dados.designacao is not None:
            starlink.alterar_designacao(Nome(dados.designacao))

        starlink_atualizado = self._repositorio.atualizar(starlink)

        return StarlinkOutput.de_entidade(starlink_atualizado)
