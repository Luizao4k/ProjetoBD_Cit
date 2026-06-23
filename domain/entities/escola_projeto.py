"""
Modulo contendo atributos Projeto de Escola
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from shared.types import EscolaId, ProjetoId, EscolaProjetoId
from domain.enums import StatusEscolaProjeto

@dataclass
class EscolaProjeto:
    """ESCOLA_PROJETO  (tabela de associação com atributos)"""
    id_escola_projeto: Optional[EscolaProjetoId]
    escola_id:         EscolaId
    projeto_id:        ProjetoId
    status:            StatusEscolaProjeto = StatusEscolaProjeto.PENDENTE
    designacao:        Optional[str]       = None
    observacao:        Optional[str]       = None
    criado_em:         datetime            = field(default_factory=datetime.now)
