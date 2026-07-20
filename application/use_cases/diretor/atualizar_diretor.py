"""
Caso de uso: atualizar um Diretor existente.
"""
from __future__ import annotations

from domain.repositories import DiretorRepository
from domain.value_objects import Email, Nome, Telefone

from .dtos import AtualizarDiretorInput, DiretorOutput
from .exceptions import DiretorNaoEncontradoError


class AtualizarDiretorUseCase:
    """
    Atualiza os dados de um Diretor já existente.

    Atualização parcial: campos não informados (None) permanecem
    inalterados.
    """

    def __init__(self, repositorio: DiretorRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dados: AtualizarDiretorInput) -> DiretorOutput:
        diretor = self._repositorio.buscar_por_id(dados.id)

        if diretor is None:
            raise DiretorNaoEncontradoError(dados.id)

        if dados.nome is not None:
            diretor.alterar_nome(Nome(dados.nome))

        if dados.telefone is not None:
            diretor.alterar_telefone(Telefone(dados.telefone))

        if dados.email is not None:
            diretor.alterar_email(Email(dados.email))

        diretor_atualizado = self._repositorio.atualizar(diretor)

        return DiretorOutput.de_entidade(diretor_atualizado)
