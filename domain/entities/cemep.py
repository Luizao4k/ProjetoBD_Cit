"""
Modulo contendo atributos Cemep
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from shared.types import CemepId, EscolaId

@dataclass
class Cemep:
    """
    CEMEP  (exclusivo de escola MUNICIPAL — validado no use case)
    """
    id_cemep:         Optional[CemepId]
    escola_id:        EscolaId
    turma:            Optional[str] = None
    nome_responsavel: Optional[str] = None
    observacao:       Optional[str] = None
    criado_em:        datetime      = field(default_factory=datetime.now)
    atualizado_em:    datetime      = field(default_factory=datetime.now)
