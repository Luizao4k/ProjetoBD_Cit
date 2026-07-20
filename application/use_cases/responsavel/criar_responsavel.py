"""
Caso de uso: criar um novo Responsável.
"""
from __future__ import annotations

from domain.entities import Responsavel
from domain.repositories import ResponsavelRepository
from domain.value_objects import Nome

from .dtos import CriarResponsavelInput, ResponsavelOutput


class CriarResponsavelUseCase:
    """
    Cria um novo Responsável vinculado a um Cemep.
    """

    def __init__(self, repositorio: ResponsavelRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dados: CriarResponsavelInput) -> ResponsavelOutput:
        responsavel = Responsavel(
            id=None,
            cemep_id=dados.cemep_id,
            nome=Nome(dados.nome),
        )

        responsavel_criado = self._repositorio.salvar(responsavel)

        return ResponsavelOutput.de_entidade(responsavel_criado)
