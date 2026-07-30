"""
CLASSE BASE DE FABRICAÇÃO TESTE PARA TODAS AS ENTIDADES
"""
from abc import ABC, abstractmethod


class BaseFactory(ABC):
    """vai servir para todas as entidades que podem ser criada ao longo do tempo."""
    @classmethod
    @abstractmethod
    def criar(cls, **kwargs):
        """Cria uma entidade válida para testes."""
        raise NotImplementedError
