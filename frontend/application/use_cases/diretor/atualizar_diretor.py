"""
Caso de uso: atualizar um Diretor existente.
"""

from __future__ import annotations

from domain.repositories import DiretorRepository
from domain.value_objects import Email, Nome, Telefone
from shared.exceptions import (
    DiretorNaoEncontradoError,
    PersistenciaInconsistenteError,
)
from shared.types import DiretorId

from .dtos import AtualizarDiretorInput, DiretorOutput


class AtualizarDiretorUseCase:
    """
    Atualiza um Diretor existente.

    A atualização é parcial: campos com valor ``None`` não são
    modificados.
    """

    def __init__(self, repositorio: DiretorRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dados: AtualizarDiretorInput) -> DiretorOutput:
        """
        Atualiza um Diretor existente.

        Args:
            dados:
                Dados necessários para a atualização.

        Returns:
            DiretorOutput contendo o estado atualizado do Diretor.

        Raises:
            DiretorNaoEncontradoError:
                Caso não exista um Diretor com o id informado.
        """

        diretor_id = DiretorId(dados.id)

        diretor = self._repositorio.buscar_por_id(diretor_id)

        if diretor is None:
            raise DiretorNaoEncontradoError(diretor_id)

        if dados.nome is not None:
            diretor.alterar_nome(Nome(dados.nome))

        if dados.telefone is not None:
            diretor.alterar_telefone(Telefone(dados.telefone))

        if dados.email is not None:
            diretor.alterar_email(Email(dados.email))

        diretor_atualizado = self._repositorio.atualizar(diretor)

        if diretor_atualizado.id is None:
            raise PersistenciaInconsistenteError(
                "O repositório retornou um Diretor sem id."
            )

        return DiretorOutput(
            id=diretor_atualizado.id,
            escola_id=diretor_atualizado.escola_id,
            nome=diretor_atualizado.nome.valor,
            telefone=diretor_atualizado.telefone.valor if diretor_atualizado.telefone else None,
            email=diretor_atualizado.email.valor if diretor_atualizado.email else None,
            criado_em=diretor_atualizado.criado_em,
            atualizado_em=diretor_atualizado.atualizado_em,
        )
