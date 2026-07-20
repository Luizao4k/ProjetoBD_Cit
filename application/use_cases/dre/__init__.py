"""
Casos de uso da DRE (Diretoria Regional de Ensino).
"""
from .criar_dre import CriarDreUseCase
from .atualizar_dre import AtualizarDreUseCase
from .remover_dre import RemoverDreUseCase
from .buscar_dre_por_id import BuscarDrePorIdUseCase
from .listar_dres import ListarDresUseCase
from .dtos import CriarDreInput, AtualizarDreInput, DreOutput
from .exceptions import DreNaoEncontradaError

__all__ = [
    "CriarDreUseCase",
    "AtualizarDreUseCase",
    "RemoverDreUseCase",
    "BuscarDrePorIdUseCase",
    "ListarDresUseCase",
    "CriarDreInput",
    "AtualizarDreInput",
    "DreOutput",
    "DreNaoEncontradaError",
]
