"""
Métodos Abstratos
"""
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
        raise NotImplementedError

    @abstractmethod
    def buscar_por_id(self, id_web_escola: int) -> Optional[WebEscola]:
        """Retorna o registro pelo id ou None se não encontrar."""
        raise NotImplementedError

    @abstractmethod
    def listar_por_escola(self, escola_id: int) -> list[WebEscola]:
        """Retorna todos os IPs de uma escola."""
        raise NotImplementedError
    @abstractmethod
    def atualizar(self, web_escola: WebEscola) -> WebEscola:
        """Persiste a alteração de IP de um registro existente."""
        raise NotImplementedError

    @abstractmethod
    def deletar(self, id_web_escola: int) -> bool:
        """
        Remove o registro pelo id.
        Retorna True se removeu, False se não encontrou.
        """
        raise NotImplementedError

    @abstractmethod
    def ip_existe_na_escola(
        self,
        escola_id: int,
        ip: str,
        ignorar_id: Optional[int] = None
        ) -> bool:
        """
        Verifica se um IP já está cadastrado para a mesma escola.
        ignorar_id é usado na edição para não conflitar com o próprio registro.
        """
        raise NotImplementedError
