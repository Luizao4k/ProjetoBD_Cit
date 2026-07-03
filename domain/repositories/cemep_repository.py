"""
Contrato de persistência da entidade Cemep.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from domain.entities import Cemep
from shared.types import CemepId, EscolaId


class CemepRepository(ABC):
    """
    Contrato que qualquer implementação de repositório
    de Cemep deve respeitar.
    """

    @abstractmethod
    def salvar(self, cemep: Cemep) -> Cemep:
        """
        Persiste um novo Cemep e retorna a entidade
        com o identificador gerado.
        """

    @abstractmethod
    def buscar_por_id(self, cemep_id: CemepId) -> Cemep | None:
        """
        Retorna o Cemep pelo identificador ou None
        caso não exista.
        """

    @abstractmethod
    def buscar_por_escola(self, escola_id: EscolaId) -> Cemep | None:
        """
        Retorna o Cemep vinculado à escola (relação 1:1)
        ou None caso a escola não possua Cemep.
        """

    @abstractmethod
    def listar_todas(self) -> list[Cemep]:
        """
        Retorna todos os Cemeps cadastrados.
        """

    @abstractmethod
    def atualizar(self, cemep: Cemep) -> Cemep:
        """
        Persiste as alterações de um Cemep e retorna
        a entidade atualizada.
        """

    @abstractmethod
    def remover(self, cemep_id: CemepId) -> None:
        """
        Remove um Cemep pelo identificador.
        """
