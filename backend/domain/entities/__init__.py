"""
Exporta todas as Entidades de domínio.
Regras:
  - Toda entidade é um dataclass com frozen=False (pode mudar estado).
  - IDs usam NewType para tipagem forte.
  - Campos opcionais usam Optional[T] explícito.
  - Nenhuma entidade conhece SQLite, HTTP ou qualquer framework.
"""

from domain.entities.diretor import Diretor
from domain.entities.escola import Escola
from domain.entities.dre import Dre
from domain.entities.cemep import Cemep
from domain.entities.chromebook import Chromebook
from domain.entities.responsavel import Responsavel
from domain.entities.starlink import Starlink
from domain.entities.turma_cemep import TurmaCemep

__all__ = [
    "Diretor",
    "Escola",
    "Dre",
    "Cemep",
    "Chromebook",
    "Responsavel",
    "Starlink",
    "TurmaCemep",
]
