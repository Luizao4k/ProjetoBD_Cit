"""
Modulo contendo atributos Diretor
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from shared.types import DiretorId, EscolaId
from shared.exceptions import RegraDeNegocioVioladaError

@dataclass
class Diretor:
    """
    DIRETOR  (0..* por escola; 1 ativo por vez — regra a ser aplicada no use case)
    """
    id_diretor: Optional[DiretorId]
    escola_id:  EscolaId
    nome:       str
    telefone:   Optional[str] = None
    email:      Optional[str] = None
    criado_em:  datetime      = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if not self.nome.strip():
            raise RegraDeNegocioVioladaError("Nome do diretor não pode ser vazio.")
