"""
DTOs (Data Transfer Objects) do caso de uso de Chromebook.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class CriarChromebookInput:
    """
    Dados necessários para criar um novo registro de Chromebook.
    """

    escola_id: int
    kit_aluno: int | None = None
    kit_professor: int | None = None


@dataclass(frozen=True, slots=True)
class AtualizarChromebookInput:
    """
    Dados utilizados para atualizar um registro de Chromebook
    existente. A atualização é parcial.
    """

    id: int
    kit_aluno: int | None = None
    kit_professor: int | None = None


@dataclass(frozen=True, slots=True)
class ChromebookOutput:
    """
    Representação de saída de um registro de Chromebook.
    """

    id: int
    escola_id: int
    kit_aluno: int | None
    kit_professor: int | None
    criado_em: datetime
    atualizado_em: datetime
