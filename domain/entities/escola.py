"""
Modulo contendo atributos Escola
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from shared.types import EscolaId, DiretorId, RegionalId
from domain.value_objects import Coordenadas, Inep
from domain.enums import TipoEscola


@dataclass
class Escola:
    """Representa uma escola cadastrada no sistema."""

    # Identidade
    id_escola: Optional[EscolaId]

    # Dados principais
    inep: Inep
    nome: str
    tipo: TipoEscola
    municipio: str

    # Relacionamentos
    diretor_id: DiretorId
    regional_id: RegionalId

    # Dados opcionais
    endereco: Optional[str] = None
    coordenadas: Optional[Coordenadas] = None
    contato: Optional[str] = None

    # Auditoria
    criado_em: datetime = field(default_factory=datetime.now)
    atualizado_em: datetime = field(default_factory=datetime.now)
