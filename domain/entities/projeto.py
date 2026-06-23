"""
Modulo contendo atributos Projeto
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from shared.types import ProjetoId
from shared.exceptions import RegraDeNegocioVioladaError

@dataclass
class Projeto:
    """PROJETO"""
    id_projeto: Optional[ProjetoId]
    nome:       str
    criado_em:  datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if not self.nome.strip():
            raise RegraDeNegocioVioladaError("Nome do projeto não pode ser vazio.")
