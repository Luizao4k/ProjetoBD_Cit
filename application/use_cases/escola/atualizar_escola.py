"""
Caso de uso: atualizar uma Escola existente.
"""
from __future__ import annotations

from domain.repositories import EscolaRepository
from domain.value_objects import Endereco, Nome

from .dtos import AtualizarEscolaInput, EscolaOutput
from .exceptions import EscolaNaoEncontradaError


class AtualizarEscolaUseCase:
    """
    Atualiza os dados de uma Escola já existente.

    Atualização parcial: campos não informados (None) permanecem
    inalterados. inep, tipo e municipio não podem ser alterados
    (são imutáveis no domínio).
    """

    def __init__(self, repositorio: EscolaRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dados: AtualizarEscolaInput) -> EscolaOutput:
        escola = self._repositorio.buscar_por_id(dados.id)

        if escola is None:
            raise EscolaNaoEncontradaError(dados.id)

        if dados.nome is not None:
            escola.alterar_nome(Nome(dados.nome))

        if dados.endereco is not None:
            escola.alterar_endereco(Endereco(dados.endereco))

        escola_atualizada = self._repositorio.atualizar(escola)

        return EscolaOutput.de_entidade(escola_atualizada)
