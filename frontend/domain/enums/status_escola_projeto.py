"""
Tipos de status de escola aceitos pelo domínio.
"""

from enum import Enum

class StatusEscolaProjeto(str, Enum):
    """
    Tipos de status: [ATIVO, INATIVO, PENDENTE]
    """
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"
    PENDENTE = "PENDENTE"
