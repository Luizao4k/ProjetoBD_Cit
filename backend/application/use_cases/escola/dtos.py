"""
DTOs (Data Transfer Objects) do caso de uso de Escola.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from ..dre.dtos import DreOutput

@dataclass(frozen=True, slots=True)
class CriarEscolaInput:
    """
    Dados necessários para criar uma nova Escola.
    """

    inep: str
    nome: str
    tipo: str
    municipio: str
    dre_id: int
    endereco: str | None = None


@dataclass(frozen=True, slots=True)
class AtualizarEscolaInput:
    """
    Dados utilizados para atualizar uma Escola existente.

    A atualização é parcial. inep, tipo e municipio não aparecem
    aqui porque são imutáveis no domínio (a entidade Escola não
    possui alterar_inep/alterar_tipo/alterar_municipio).
    """

    id: int
    nome: str | None = None
    endereco: str | None = None


@dataclass(frozen=True, slots=True)
class EscolaOutput:
    """
    Representação de saída de uma Escola.
    """

    id: int
    inep: str
    nome: str
    tipo: str
    municipio: str
    dre_id: int
    endereco: str | None
    dre: DreOutput | None
    criado_em: datetime
    atualizado_em: datetime
