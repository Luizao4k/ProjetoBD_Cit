"""
Modulo contendo atributos Regional
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from shared.types import RegionalId
from shared.exceptions import RegraDeNegocioVioladaError

@dataclass
class Regional:
    """
    Diretoria Regional de Ensino.
    Uma DRE agrupa várias escolas de uma região.
    """
    regional_id:    Optional[RegionalId]
    nome:           str
    municipio_sede: Optional[str]  = None
    criado_em:      datetime       = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if not self.nome.strip():
            raise RegraDeNegocioVioladaError("Nome da DRE não pode ser vazio.")
