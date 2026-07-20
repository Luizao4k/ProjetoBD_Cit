"""
Casos de uso da Escola.
"""
from .criar_escola import CriarEscolaUseCase
from .buscar_escola_por_id import BuscarEscolaPorIdUseCase
from .buscar_escolas_por_dre import BuscarEscolasPorDreUseCase
from .listar_escolas import ListarEscolasUseCase
from .atualizar_escola import AtualizarEscolaUseCase
from .remover_escola import RemoverEscolaUseCase
from .dtos import CriarEscolaInput, AtualizarEscolaInput, EscolaOutput
from .exceptions import EscolaNaoEncontradaError

__all__ = [
    "CriarEscolaUseCase",
    "BuscarEscolaPorIdUseCase",
    "BuscarEscolasPorDreUseCase",
    "ListarEscolasUseCase",
    "AtualizarEscolaUseCase",
    "RemoverEscolaUseCase",
    "CriarEscolaInput",
    "AtualizarEscolaInput",
    "EscolaOutput",
    "EscolaNaoEncontradaError",
]
