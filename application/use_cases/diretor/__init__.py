"""
Casos de uso do Diretor.
"""
from .criar_diretor import CriarDiretorUseCase
from .buscar_diretor_por_id import BuscarDiretorPorIdUseCase
from .buscar_diretor_por_escola import BuscarDiretorPorEscolaUseCase
from .listar_diretores import ListarDiretoresUseCase
from .atualizar_diretor import AtualizarDiretorUseCase
from .remover_diretor import RemoverDiretorUseCase
from .dtos import CriarDiretorInput, AtualizarDiretorInput, DiretorOutput
from .exceptions import DiretorNaoEncontradoError

__all__ = [
    "CriarDiretorUseCase",
    "BuscarDiretorPorIdUseCase",
    "BuscarDiretorPorEscolaUseCase",
    "ListarDiretoresUseCase",
    "AtualizarDiretorUseCase",
    "RemoverDiretorUseCase",
    "CriarDiretorInput",
    "AtualizarDiretorInput",
    "DiretorOutput",
    "DiretorNaoEncontradoError",
]
