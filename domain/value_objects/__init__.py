"""
O arquivo serve para transformar a pasta em um pacote Python e, opcionalmente,
expor os Value Objects que você deseja importar diretamente.
"""
from .coordenadas import Coordenadas
from .inep import Inep

__all__ = [
    "Coordenadas",
    "Inep",
]
