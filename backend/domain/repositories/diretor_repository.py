"""
Contrato de persistência da entidade Diretor.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from backend.domain.entities import Diretor
from backend.shared.types import DiretorId, EscolaId


class DiretorRepository(ABC):
    """
    Contrato que qualquer implementação de repositório
    de diretor deve respeitar.
    """
    @abstractmethod
    def salvar(self, diretor: Diretor) -> Diretor:
        """
        Persiste um novo diretor e retorna a entidade
        com o identificador gerado.
        """

    @abstractmethod
    def buscar_por_id(self, diretor_id: DiretorId) -> Diretor | None:
        """
        Retorna o diretor pelo identificador ou None
        caso não exista.
        """

    @abstractmethod
    def buscar_por_escola(self, escola_id: EscolaId) -> Diretor | None:
        """
        Retorna o diretor vinculado à escola (relação 1:1)
        ou None caso a escola não possua diretor.
        """

    @abstractmethod
    def listar_todas(self) -> list[Diretor]:
        """
        Retorna todos os diretores cadastrados.
        """

    @abstractmethod
    def atualizar(self, diretor: Diretor) -> Diretor:
        """
        Persiste as alterações de um diretor e retorna
        a entidade atualizada.
        """

    @abstractmethod
    def remover(self, diretor_id: DiretorId) -> None:
        """
        Remove um diretor pelo identificador.
        """

