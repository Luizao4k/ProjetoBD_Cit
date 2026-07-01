"""
O arquivo serve para expor os repositorios do domínio.
"""
from domain.repositories.diretor_repository import DiretorRepository
from domain.repositories.dre_repository import DreRepository
from domain.repositories.escola_repository import EscolaRepository

__all__ = ["DiretorRepository", "DreRepository", "EscolaRepository"]
