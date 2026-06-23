"""
Tipos de escola aceitos pelo domínio.
"""

from enum import Enum


class TipoEscola(str, Enum):
    """
    Tipos: ESTADUAL | MUNICIPAL
    """
    ESTADUAL = "ESTADUAL"
    MUNICIPAL = "MUNICIPAL"
