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
        ...

    @abstractmethod
    def buscar_por_id(self, id: int) -> Optional[Regional]:
        """Retorna a regional pelo id ou None se não encontrar."""
        ...

    @abstractmethod
    def buscar_por_tipo(self, tipo: str) -> list[Regional]:
        """Retorna todas as regionais de um tipo: 'DRE' ou 'NTE'."""
        ...

    @abstractmethod
    def listar_todas(self) -> list[Regional]:
        """Retorna todas as regionais cadastradas."""
        ...

    @abstractmethod
    def atualizar(self, regional: Regional) -> Regional:
        """Persiste as alterações de uma regional existente."""
        ...

    @abstractmethod
    def deletar(self, id: int) -> bool:
        """
        Remove a regional pelo id.
        Retorna True se removeu, False se não encontrou.
        Deve lançar erro se houver escolas vinculadas.
        """
        ...

    @abstractmethod
    def tem_escolas_vinculadas(self, id: int) -> bool:
        """Verifica se a regional possui escolas antes de deletar."""
        ...
