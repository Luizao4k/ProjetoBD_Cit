"""
Contrato de persistência da entidade Diretor.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from domain.entities import Diretor
from shared.types import DiretorId


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
        Retorna a diretor pelo identificador ou None
        caso não exista.
        """

    @abstractmethod
    def listar(self) -> list[Diretor]:
        """
        Retorna todos os diretores cadastradas.
        """

    @abstractmethod
    def remover(self, diretor_id: DiretorId) -> None:
        """
        Remove um diretor pelo identificador.
        """
