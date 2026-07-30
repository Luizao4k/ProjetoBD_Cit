"""
DTOs (Data Transfer Objects) do caso de uso de TurmaCemep.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class CriarTurmaCemepInput:
    """
    Dados necessários para criar uma nova Turma do Cemep.
    """

    responsavel_id: int
    nome_turma: str


@dataclass(frozen=True, slots=True)
class AtualizarTurmaCemepInput:
    """
    Dados utilizados para atualizar uma Turma existente.

    A atualização é parcial. responsavel_id não aparece aqui —
    trocar o responsável de uma turma não é uma operação
    suportada pelo domínio.
    """

    id: int
    nome_turma: str | None = None


@dataclass(frozen=True, slots=True)
class TurmaCemepOutput:
    """
    Representação de saída de uma Turma do Cemep.
    """

    id: int
    responsavel_id: int
    nome_turma: str
    criado_em: datetime
    atualizado_em: datetime
