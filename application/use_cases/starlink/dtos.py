"""
DTOs (Data Transfer Objects) do caso de uso de Starlink.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class CriarStarlinkInput:
    """
    Dados necessários para criar uma nova designação de Starlink.
    """

    escola_id: int
    designacao: str


@dataclass(frozen=True, slots=True)
class AtualizarStarlinkInput:
    """
    Dados utilizados para atualizar uma designação existente.

    A atualização é parcial. escola_id não aparece aqui — trocar a
    escola de uma designação não é uma operação suportada pelo
    domínio.
    """

    id: int
    designacao: str | None = None


@dataclass(frozen=True, slots=True)
class StarlinkOutput:
    """
    Representação de saída de uma designação de Starlink.
    """

    id: int
    escola_id: int
    designacao: str
    criado_em: datetime
    atualizado_em: datetime
