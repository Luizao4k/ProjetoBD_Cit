"""
Caso de uso: criar um novo Cemep.
"""

from __future__ import annotations

from domain.entities import Cemep
from domain.repositories import CemepRepository
from domain.value_objects import Comentario
from shared.exceptions import PersistenciaInconsistenteError
from shared.types import EscolaId

from .dtos import CriarCemepInput, CemepOutput


class CriarCemepUseCase:
    """
    Cria um novo Cemep vinculado a uma escola.

    A verificação de unicidade (uma escola possuir apenas um
    Cemep) é responsabilidade da camada de persistência.
    """

    def __init__(self, repositorio: CemepRepository) -> None:
        """
        Inicializa o caso de uso.

        Args:
            repositorio:
                Repositório responsável pela persistência dos Cemep.
        """
        self._repositorio = repositorio

    def executar(self, dados: CriarCemepInput) -> CemepOutput:
        """
        Cria um novo Cemep.

        Args:
            dados:
                Dados necessários para a criação do Cemep.

        Returns:
            DTO contendo os dados do Cemep criado.

        Raises:
            PersistenciaInconsistenteError:
                Caso o repositório retorne uma entidade persistida
                em estado inconsistente.
        """

        # Cria a entidade de domínio.
        cemep = Cemep(
            id=None,
            escola_id=EscolaId(dados.escola_id),
            comentario=Comentario(dados.comentario) if dados.comentario else None,
        )

        # Persiste a entidade.
        cemep_criado = self._repositorio.salvar(cemep)

        # Garante que a entidade retornada pelo repositório está
        # devidamente persistida.
        if cemep_criado.id is None:
            raise PersistenciaInconsistenteError(
                "O repositório retornou um Cemep sem id."
            )

        # Converte a entidade de domínio para o DTO de saída.
        return CemepOutput(
            id=cemep_criado.id,
            escola_id=cemep_criado.escola_id,
            comentario=cemep_criado.comentario.valor if cemep_criado.comentario else None,
            criado_em=cemep_criado.criado_em,
            atualizado_em=cemep_criado.atualizado_em,
        )