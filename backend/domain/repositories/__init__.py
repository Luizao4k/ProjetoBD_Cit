"""
O arquivo serve para expor os repositorios do domínio.
"""
from domain.repositories.diretor_repository import DiretorRepository
from domain.repositories.dre_repository import DreRepository
from domain.repositories.escola_repository import EscolaRepository
from domain.repositories.cemep_repository import CemepRepository
from domain.repositories.chromebook_repository import ChromebookRepository
from domain.repositories.responsavel_repository import ResponsavelRepository
from domain.repositories.starlink_repository import StarlinkRepository
from domain.repositories.turma_cemep_repository import TurmaCemepRepository

__all__ = ["DiretorRepository",
           "DreRepository",
           "EscolaRepository",
           "CemepRepository",
           "ChromebookRepository",
           "ResponsavelRepository",
           "StarlinkRepository",
           "TurmaCemepRepository",
           ]
