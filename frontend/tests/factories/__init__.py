"""
Factories utilizadas nos testes.

As factories criam entidades de domínio válidas para facilitar a escrita
dos testes, evitando repetição de código.
"""

from .base_factory import BaseFactory
from .cemep_factory import CemepFactory
from .chromebook_factory import ChromebookFactory
from .diretor_factory import DiretorFactory
from .dre_factory import DreFactory
from .escola_factory import EscolaFactory
from .responsavel_factory import ResponsavelFactory
from .starlink_factory import StarlinkFactory
from .turma_cemep_factory import TurmaCemepFactory

__all__ = [
    "BaseFactory",
    "CemepFactory",
    "ChromebookFactory",
    "DiretorFactory",
    "DreFactory",
    "EscolaFactory",
    "ResponsavelFactory",
    "StarlinkFactory",
    "TurmaCemepFactory",
]