"""
O arquivo serve para transformar a pasta em um pacote Python e, opcionalmente,
expor os Value Objects que você deseja importar diretamente.
"""
from .inep import Inep
from .nome import Nome
from .telefone import Telefone
from .email import Email
from .municipio import Municipio
from .endereco import Endereco

__all__ = [
    "Inep", 
    "Nome",
    "Telefone",
    "Email",
    "Municipio",
    "Endereco"
]
