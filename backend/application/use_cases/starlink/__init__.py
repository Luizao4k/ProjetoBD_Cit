"""
Casos de uso do Starlink.
"""
from .criar_starlink import CriarStarlinkUseCase
from .buscar_starlink_por_id import BuscarStarlinkPorIdUseCase
from .buscar_starlinks_por_escola import BuscarStarlinksPorEscolaUseCase
from .listar_starlinks import ListarStarlinksUseCase
from .atualizar_starlink import AtualizarStarlinkUseCase
from .remover_starlink import RemoverStarlinkUseCase
from .dtos import CriarStarlinkInput, AtualizarStarlinkInput, StarlinkOutput


__all__ = [
    "CriarStarlinkUseCase",
    "BuscarStarlinkPorIdUseCase",
    "BuscarStarlinksPorEscolaUseCase",
    "ListarStarlinksUseCase",
    "AtualizarStarlinkUseCase",
    "RemoverStarlinkUseCase",
    "CriarStarlinkInput",
    "AtualizarStarlinkInput",
    "StarlinkOutput",
]
