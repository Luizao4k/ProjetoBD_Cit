"""
O arquivo serve para transformar a pasta em um pacote Python e,
expor os Enums do domínio.
"""

from .tipo_escola import TipoEscola
from .status_escola_projeto import StatusEscolaProjeto

__all__ = [
    "TipoEscola",
    "StatusEscolaProjeto",
]
