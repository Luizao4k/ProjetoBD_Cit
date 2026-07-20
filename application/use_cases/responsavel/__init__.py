"""
Casos de uso do Responsável.
"""
from .criar_responsavel import CriarResponsavelUseCase
from .buscar_responsavel_por_id import BuscarResponsavelPorIdUseCase
from .buscar_responsaveis_por_cemep import BuscarResponsaveisPorCemepUseCase
from .listar_responsaveis import ListarResponsaveisUseCase
from .atualizar_responsavel import AtualizarResponsavelUseCase
from .remover_responsavel import RemoverResponsavelUseCase
from .dtos import (
    CriarResponsavelInput,
    AtualizarResponsavelInput,
    ResponsavelOutput,
)
from .exceptions import ResponsavelNaoEncontradoError

__all__ = [
    "CriarResponsavelUseCase",
    "BuscarResponsavelPorIdUseCase",
    "BuscarResponsaveisPorCemepUseCase",
    "ListarResponsaveisUseCase",
    "AtualizarResponsavelUseCase",
    "RemoverResponsavelUseCase",
    "CriarResponsavelInput",
    "AtualizarResponsavelInput",
    "ResponsavelOutput",
    "ResponsavelNaoEncontradoError",
]
