"""
Contrato de persistência da entidade DRE.
"""

from abc import ABC, abstractmethod

from domain.entities import Dre
from shared.types import DreId


class DreRepository(ABC):
    """
    Contrato que qualquer implementação de repositório
    de DRE deve respeitar.
    """

    @abstractmethod
    def salvar(self, dre: Dre) -> Dre:
        """
        Persiste uma nova DRE e retorna a entidade
        com o identificador gerado.
        """

    @abstractmethod
    def buscar_por_id(self, dre_id: DreId) -> Dre | None:
        """
        Retorna a DRE pelo identificador ou None
        caso não exista.
        """

    @abstractmethod
    def listar_todas(self) -> list[Dre]:
        """
        Retorna todas as DREs cadastradas.
        """

    @abstractmethod
    def atualizar(self, dre: Dre) -> Dre:
        """
        Persiste as alterações de uma DRE e retorna
        a entidade atualizada.
        """

    @abstractmethod
    def remover(self, dre_id: DreId) -> None:
        """
        Remove uma DRE pelo identificador.
        """
