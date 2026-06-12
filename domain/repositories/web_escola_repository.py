from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.web_escola import WebEscola


class WebEscolaRepository(ABC):
    """
    Contrato para gerenciamento dos IPs de webEscola.
    Uma escola pode ter zero ou vários IPs associados.
    """

    @abstractmethod
    def salvar(self, web_escola: WebEscola) -> WebEscola:
        """Persiste um novo IP e retorna com o id gerado."""
        ...

    @abstractmethod
    def buscar_por_id(self, id: int) -> Optional[WebEscola]:
        """Retorna o registro pelo id ou None se não encontrar."""
        ...

    @abstractmethod
    def listar_por_escola(self, escola_id: int) -> list[WebEscola]:
        """Retorna todos os IPs de uma escola."""
        ...

    @abstractmethod
    def atualizar(self, web_escola: WebEscola) -> WebEscola:
        """Persiste a alteração de IP de um registro existente."""
        ...

    @abstractmethod
    def deletar(self, id: int) -> bool:
        """
        Remove o registro pelo id.
        Retorna True se removeu, False se não encontrou.
        """
        ...

    @abstractmethod
    def ip_existe_na_escola(self, escola_id: int, ip: str, ignorar_id: Optional[int] = None) -> bool:
        """
        Verifica se um IP já está cadastrado para a mesma escola.
        ignorar_id é usado na edição para não conflitar com o próprio registro.
        """
        ...