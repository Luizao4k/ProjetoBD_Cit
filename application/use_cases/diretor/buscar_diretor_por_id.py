"""
Caso de uso: buscar um Diretor pelo identificador.
"""

from __future__ import annotations

from domain.repositories import DiretorRepository
from shared.exceptions import (
    DiretorNaoEncontradoError,
    PersistenciaInconsistenteError,
)
from shared.types import DiretorId

from .dtos import DiretorOutput


class BuscarDiretorPorIdUseCase:
    """
    Busca um Diretor pelo seu identificador.
    """

    def __init__(self, repositorio: DiretorRepository) -> None:
        """
        Inicializa o caso de uso.

        Args:
            repositorio:
                Repositório responsável pela persistência dos Diretores.
        """
        self._repositorio = repositorio

    def executar(self, diretor_id: int) -> DiretorOutput:
        """
        Busca um Diretor pelo identificador.

        Args:
            diretor_id:
                Identificador do Diretor.

        Returns:
            DTO contendo os dados do Diretor.

        Raises:
            DiretorNaoEncontradoError:
                Caso não exista um Diretor com o id informado.

            PersistenciaInconsistenteError:
                Caso o repositório retorne uma entidade persistida
                em estado inconsistente.
        """

        diretor_id = DiretorId(diretor_id)

        diretor = self._repositorio.buscar_por_id(diretor_id)

        if diretor is None:
            raise DiretorNaoEncontradoError(diretor_id)

        if diretor.id is None:
            raise PersistenciaInconsistenteError(
                "O repositório retornou um Diretor sem id."
            )

        return DiretorOutput(
            id=diretor.id,
            escola_id=diretor.escola_id,
            nome=diretor.nome.valor,
            telefone=diretor.telefone.valor if diretor.telefone else None,
            email=diretor.email.valor if diretor.email else None,
            criado_em=diretor.criado_em,
            atualizado_em=diretor.atualizado_em,
        )
