"""
Contrato de persistência da entidade TurmaCemep.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from domain.entities import TurmaCemep
from shared.types import ResponsavelId, TurmaCemepId


class TurmaCemepRepository(ABC):
    """
    Contrato que qualquer implementação de repositório
    de TurmaCemep deve respeitar.
    """

    @abstractmethod
    def salvar(self, turma: TurmaCemep) -> TurmaCemep:
        """
        Persiste uma nova turma e retorna a entidade
        com o identificador gerado.
        """

    @abstractmethod
    def buscar_por_id(self, turma_id: TurmaCemepId) -> TurmaCemep | None:
        """
        Retorna a turma pelo identificador ou None
        caso não exista.
        """

    @abstractmethod
    def buscar_por_responsavel(
        self, responsavel_id: ResponsavelId
    ) -> list[TurmaCemep]:
        """
        Retorna todas as turmas vinculadas ao responsável
        (relação 1:N).
        """

    @abstractmethod
    def listar_todas(self) -> list[TurmaCemep]:
        """
        Retorna todas as turmas cadastradas.
        """

    @abstractmethod
    def atualizar(self, turma: TurmaCemep) -> TurmaCemep:
        """
        Persiste as alterações de uma turma e retorna
        a entidade atualizada.
        """

    @abstractmethod
    def remover(self, turma_id: TurmaCemepId) -> None:
        """
        Remove uma turma pelo identificador.
        """
