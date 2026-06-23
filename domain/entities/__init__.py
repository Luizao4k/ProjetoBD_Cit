"""
Exporta todas as Entidades de domínio.
Regras:
  - Toda entidade é um dataclass com frozen=False (pode mudar estado).
  - IDs usam NewType para tipagem forte.
  - Campos opcionais usam Optional[T] explícito.
  - Nenhuma entidade conhece SQLite, HTTP ou qualquer framework.
"""

from domain.entities.cemep import Cemep
from domain.entities.diretor import Diretor
from domain.entities.escola_projeto import EscolaProjeto
from domain.entities.escola import Escola
from domain.entities.projeto import Projeto
from domain.entities.regional import Regional

__all__ = ["Cemep", "Diretor", "EscolaProjeto", "Escola", "Projeto", "Regional"]
