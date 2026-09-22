"""
Contrato de persistência da entidade Starlink.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from domain.entities import Starlink
from shared.types import EscolaId, StarlinkId


class StarlinkRepository(ABC):
    """
    Contrato que qualquer implementação de repositório
    de Starlink deve respeitar.
    """

    @abstractmethod
    def salvar(self, starlink: Starlink) -> Starlink:
        """
        Persiste uma nova designação de Starlink e retorna
        a entidade com o identificador gerado.
        """

    @abstractmethod
    def buscar_por_id(self, starlink_id: StarlinkId) -> Starlink | None:
        """
        Retorna a designação de Starlink pelo identificador
        ou None caso não exista.
        """

    @abstractmethod
    def buscar_por_escola(self, escola_id: EscolaId) -> list[Starlink]:
        """
        Retorna todas as designações de Starlink vinculadas
        à escola (relação 1:N).
        """

    @abstractmethod
    def buscar_por_designacao(self, designacao: str,) -> Starlink | None:
        """
        Retorna a Starlink pela designação ou None caso
        não exista uma designação igual.
        """


    @abstractmethod
    def listar_todas(self) -> list[Starlink]:
        """
        Retorna todas as designações de Starlink cadastradas.
        """

    @abstractmethod
    def atualizar(self, starlink: Starlink) -> Starlink:
        """
        Persiste as alterações de uma designação de Starlink
        e retorna a entidade atualizada.
        """

    @abstractmethod
    def remover(self, starlink_id: StarlinkId) -> None:
        """
        Remove uma designação de Starlink pelo identificador.
        """
