"""
DTOs (Data Transfer Objects) do caso de uso de Responsavel.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class CriarResponsavelInput:
    """
    Dados necessários para criar um novo Responsável.
    """

    cemep_id: int
    nome: str


@dataclass(frozen=True, slots=True)
class AtualizarResponsavelInput:
    """
    Dados utilizados para atualizar um Responsável existente.

    A atualização é parcial. cemep_id não aparece aqui — trocar o
    Cemep de um responsável não é uma operação suportada pelo
    domínio.
    """

    id: int
    nome: str | None = None


@dataclass(frozen=True, slots=True)
class ResponsavelOutput:
    """
    Representação de saída de um Responsável.
    """

    id: int
    cemep_id: int
    nome: str
    criado_em: datetime
    atualizado_em: datetime
