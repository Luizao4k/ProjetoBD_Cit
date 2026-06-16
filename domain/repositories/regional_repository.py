"""
Métodos Abstratos
"""
from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.regional import Regional


class RegionalRepository(ABC):
    """
    Contrato que qualquer implementação de repositório
    de Regional precisa respeitar.

    O domain não sabe se o dado vem do SQLite, PostgreSQL
    ou de uma lista em memória — isso é detalhe de infraestrutura.
    """

    @abstractmethod
    def salvar(self, regional: Regional) -> Regional:
        """Persiste uma nova regional e retorna com o id gerado."""
        raise NotImplementedError

    @abstractmethod
    def buscar_por_id(self, regional_id: int) -> Optional[Regional]:
        """Retorna a regional pelo id ou None se não encontrar."""
        raise NotImplementedError

    @abstractmethod
    def buscar_por_tipo(self, tipo: str) -> list[Regional]:
        """Retorna todas as regionais de um tipo: 'DRE' ou 'NTE'."""
        raise NotImplementedError

    @abstractmethod
    def listar_todas(self) -> list[Regional]:
        """Retorna todas as regionais cadastradas."""
        raise NotImplementedError

    @abstractmethod
    def atualizar(self, regional: Regional) -> Regional:
        """Persiste as alterações de uma regional existente."""
        raise NotImplementedError

    @abstractmethod
    def deletar(self, regional_id: int) -> bool:
        """
        Remove a regional pelo id.
        Retorna True se removeu, False se não encontrou.
        Deve lançar erro se houver escolas vinculadas.
        """
        raise NotImplementedError

    @abstractmethod
    def tem_escolas_vinculadas(self, regional_id: int) -> bool:
        """Verifica se a regional possui escolas antes de deletar."""
        raise NotImplementedError
