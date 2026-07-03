"""
O arquivo serve para transformar a pasta em um pacote Python e, opcionalmente,
expor os responsabilidades que você deseja 
"""
from .entidade_constantes import ENTITY_DIRETOR, ENTITY_DRE, ENTITY_ESCOLA
from .limite import MAX_LEN
from .municipios_validos import MUNICIPIOS_VALIDOS

__all__ = ["ENTITY_DRE",
           "ENTITY_ESCOLA", 
           "ENTITY_DIRETOR",
           "MUNICIPIOS_VALIDOS",
           "MAX_LEN",
           ]
