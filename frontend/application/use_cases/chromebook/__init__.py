"""
Casos de uso do Chromebook.
"""
from .criar_chromebook import CriarChromebookUseCase
from .buscar_chromebook_por_id import BuscarChromebookPorIdUseCase
from .buscar_chromebook_por_escola import BuscarChromebookPorEscolaUseCase
from .listar_chromebooks import ListarChromebooksUseCase
from .atualizar_chromebook import AtualizarChromebookUseCase
from .remover_chromebook import RemoverChromebookUseCase
from .dtos import (
    CriarChromebookInput,
    AtualizarChromebookInput,
    ChromebookOutput,
)


__all__ = [
    "CriarChromebookUseCase",
    "BuscarChromebookPorIdUseCase",
    "BuscarChromebookPorEscolaUseCase",
    "ListarChromebooksUseCase",
    "AtualizarChromebookUseCase",
    "RemoverChromebookUseCase",
    "CriarChromebookInput",
    "AtualizarChromebookInput",
    "ChromebookOutput",
]
