"""
Caso de uso: criar uma nova DRE.
"""

from __future__ import annotations

from domain.entities import Dre
from domain.repositories import DreRepository
from domain.value_objects import Nome, Telefone
from shared.exceptions import PersistenciaInconsistenteError

from .dtos import CriarDreInput, DreOutput


class CriarDreUseCase:
    """
    Cria uma nova DRE.
    """

    def __init__(self, repositorio: DreRepository) -> None:
        """
        Inicializa o caso de uso.

        Args:
            repositorio:
                Repositório responsável pela persistência das DREs.
        """
        self._repositorio = repositorio

    def executar(self, dados: CriarDreInput) -> DreOutput:
        """
        Cria uma nova DRE.

        Args:
            dados:
                Dados necessários para a criação da DRE.

        Returns:
            DTO contendo os dados da DRE criada.

        Raises:
            PersistenciaInconsistenteError:
                Caso o repositório retorne uma entidade persistida
                em estado inconsistente.
        """

        # Cria a entidade de domínio.
        dre = Dre(
            id=None,
            nome=Nome(dados.nome),
            telefone=Telefone(dados.telefone) if dados.telefone else None,
        )

        # Persiste a entidade.
        dre_criada = self._repositorio.salvar(dre)

        # Garante que a entidade retornada pelo repositório está
        # devidamente persistida.
        if dre_criada.id is None:
            raise PersistenciaInconsistenteError(
                "O repositório retornou uma DRE sem id."
            )

        # Converte a entidade de domínio para o DTO de saída.
        return DreOutput(
            id=dre_criada.id,
            nome=dre_criada.nome.valor,
            telefone=dre_criada.telefone.valor if dre_criada.telefone else None,
            criado_em=dre_criada.criado_em,
            atualizado_em=dre_criada.atualizado_em,
        )
