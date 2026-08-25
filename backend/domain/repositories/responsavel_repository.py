"""
Contrato de persistência da entidade Responsavel.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from backend.domain.entities import Responsavel
from backend.shared.types import CemepId, ResponsavelId


class ResponsavelRepository(ABC):
    """
    Contrato que qualquer implementação de repositório
    de Responsavel deve respeitar.
    """

    @abstractmethod
    def salvar(self, responsavel: Responsavel) -> Responsavel:
        """
        Persiste um novo responsável e retorna a entidade
        com o identificador gerado.
        """

    @abstractmethod
    def buscar_por_id(self, responsavel_id: ResponsavelId) -> Responsavel | None:
        """
        Retorna o responsável pelo identificador ou None
        caso não exista.
        """

    @abstractmethod
    def buscar_por_cemep(self, cemep_id: CemepId) -> list[Responsavel]:
        """
        Retorna todos os responsáveis vinculados ao Cemep
        (relação 1:N).
        """

    @abstractmethod
    def listar_todas(self) -> list[Responsavel]:
        """
        Retorna todos os responsáveis cadastrados.
        """

    @abstractmethod
    def atualizar(self, responsavel: Responsavel) -> Responsavel:
        """
        Persiste as alterações de um responsável e retorna
        a entidade atualizada.
        """

    @abstractmethod
    def remover(self, responsavel_id: ResponsavelId) -> None:
        """
        Remove um responsável pelo identificador.
        """
