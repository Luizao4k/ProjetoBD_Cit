"""
Métodos Abstratos da entidade Escola
"""
from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.escola import Escola


class EscolaRepository(ABC):
    """
    Contrato que qualquer implementação de repositório
    de Escola precisa respeitar.
    """

    @abstractmethod
    def salvar(self, escola: Escola) -> Escola:
        """Persiste uma nova escola e retorna com o id gerado."""
        raise NotImplementedError

    @abstractmethod
    def buscar_por_id(self, id_escola: int) -> Optional[Escola]:
        """Retorna a escola pelo id ou None se não encontrar."""
        raise NotImplementedError

    @abstractmethod
    def buscar_por_inep(self, inep: str) -> Optional[Escola]:
        """Retorna a escola pelo INEP ou None se não encontrar."""
        raise NotImplementedError

    @abstractmethod
    def buscar_por_regional(self, regional_id: int) -> list[Escola]:
        """Retorna todas as escolas de uma regional."""
        raise NotImplementedError

    @abstractmethod
    def listar_todas(self) -> list[Escola]:
        """Retorna todas as escolas cadastradas."""
        raise NotImplementedError

    @abstractmethod
    def buscar_com_filtros(
        self,
        regional_id: Optional[int] = None,
        tipo_regional: Optional[str] = None,
        busca: Optional[str] = None,
    ) -> list[Escola]:
        """
        Retorna escolas aplicando filtros combinados.
        - regional_id : filtra por regional específica
        - tipo_regional: 'DRE' ou 'NTE'
        - busca       : texto livre que busca em nomeEscola e INEP
        """
        raise NotImplementedError

    @abstractmethod
    def atualizar(self, escola: Escola) -> Escola:
        """Persiste as alterações de uma escola existente."""
        raise NotImplementedError

    @abstractmethod
    def deletar(self, id_escola: int) -> bool:
        """
        Remove a escola pelo id.
        Retorna True se removeu, False se não encontrou.
        """
        raise NotImplementedError

    @abstractmethod
    def inep_existe(self, inep: str, ignorar_id: Optional[int] = None) -> bool:
        """
        Verifica se um INEP já está cadastrado.
        ignorar_id é usado na edição para não conflitar com o próprio registro.
        """
        raise NotImplementedError
