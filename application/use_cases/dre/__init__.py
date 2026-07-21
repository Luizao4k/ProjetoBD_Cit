"""
Casos de uso da DRE (Diretoria Regional de Ensino).
"""
from .criar_dre import CriarDreUseCase
from .buscar_dre_por_id import BuscarDrePorIdUseCase
from .listar_dres import ListarDresUseCase
from .atualizar_dre import AtualizarDreUseCase
from .remover_dre import RemoverDreUseCase
from .dtos import CriarDreInput, AtualizarDreInput, DreOutput


__all__ = [
    "CriarDreUseCase",
    "BuscarDrePorIdUseCase",
    "ListarDresUseCase",
    "AtualizarDreUseCase",
    "RemoverDreUseCase",
    "CriarDreInput",
    "AtualizarDreInput",
    "DreOutput",
]
