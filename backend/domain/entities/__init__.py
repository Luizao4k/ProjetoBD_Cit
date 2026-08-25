"""
Exporta todas as Entidades de domínio.
Regras:
  - Toda entidade é um dataclass com frozen=False (pode mudar estado).
  - IDs usam NewType para tipagem forte.
  - Campos opcionais usam Optional[T] explícito.
  - Nenhuma entidade conhece SQLite, HTTP ou qualquer framework.
"""

from backend.domain.entities.diretor import Diretor
from backend.domain.entities.escola import Escola
from backend.domain.entities.dre import Dre
from backend.domain.entities.cemep import Cemep
from backend.domain.entities.chromebook import Chromebook
from backend.domain.entities.responsavel import Responsavel
from backend.domain.entities.starlink import Starlink
from backend.domain.entities.turma_cemep import TurmaCemep

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
