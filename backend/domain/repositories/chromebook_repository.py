"""
Contrato de persistência da entidade Chromebook.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from backend.domain.entities import Chromebook
from backend.shared.types import ChromebooksId, EscolaId


class ChromebookRepository(ABC):
    """
    Contrato que qualquer implementação de repositório
    de Chromebook deve respeitar.
    """

    @abstractmethod
    def salvar(self, chromebook: Chromebook) -> Chromebook:
        """
        Persiste um novo registro de Chromebook e retorna a
        entidade com o identificador gerado.
        """

    @abstractmethod
    def buscar_por_id(self, chromebook_id: ChromebooksId) -> Chromebook | None:
        """
        Retorna o registro de Chromebook pelo identificador
        ou None caso não exista.
        """

    @abstractmethod
    def buscar_por_escola(self, escola_id: EscolaId) -> Chromebook | None:
        """
        Retorna o registro de Chromebook vinculado à escola
        (relação 1:1) ou None caso a escola não possua registro.
        """

    @abstractmethod
    def listar_todas(self) -> list[Chromebook]:
        """
        Retorna todos os registros de Chromebook cadastrados.
        """

    @abstractmethod
    def atualizar(self, chromebook: Chromebook) -> Chromebook:
        """
        Persiste as alterações de um registro de Chromebook
        e retorna a entidade atualizada.
        """

    @abstractmethod
    def remover(self, chromebook_id: ChromebooksId) -> None:
        """
        Remove um registro de Chromebook pelo identificador.
        """
