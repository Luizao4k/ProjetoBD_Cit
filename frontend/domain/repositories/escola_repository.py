"""
Contrato de persistência da entidade Escola.
"""

from abc import ABC, abstractmethod

from domain.entities import Escola
from domain.value_objects import Inep, Nome
from shared.types import DreId, EscolaId


class EscolaRepository(ABC):
    """
    Contrato que qualquer implementação de repositório
    de Escola deve respeitar.
    """

    @abstractmethod
    def salvar(self, escola: Escola) -> Escola:
        """
        Persiste uma nova escola e retorna a entidade
        com o identificador gerado.
        """

    @abstractmethod
    def buscar_por_id(self, escola_id: EscolaId) -> Escola | None:
        """
        Retorna a escola pelo identificador ou None
        caso não exista.
        """

    @abstractmethod
    def buscar_por_nome(self, nome: Nome) -> list[Escola]:
        """
        Retorna a escola pelo nome ou uma lista vazia
        caso não exista
        """

    @abstractmethod
    def buscar_por_inep(self, inep: Inep) -> Escola | None:
        """
        Retorna a escola pelo INEP ou None
        caso não exista.
        """

    @abstractmethod
    def buscar_por_municipio(self, municipio: str) -> list[Escola]:
        """
        Retorna todas as escolas de um município.
        """

    @abstractmethod
    def buscar_por_dre(self, dre_id: DreId) -> list[Escola]:
        """
        Retorna todas as escolas vinculadas à DRE.
        """

    @abstractmethod
    def listar_todas(self) -> list[Escola]:
        """
        Retorna todas as escolas cadastradas.
        """

    @abstractmethod
    def atualizar(self, escola: Escola) -> Escola:
        """
        Persiste as alterações de uma escola e retorna
        a entidade atualizada.
        """

    @abstractmethod
    def remover(self, escola_id: EscolaId) -> None:
        """
        Remove uma escola pelo identificador.
        """
