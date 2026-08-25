"""
Modulo contendo atributos Escola
"""

from __future__ import annotations

from dataclasses import dataclass

from backend.shared.types import EscolaId, DreId
from backend.domain.value_objects import Inep, Nome, Municipio, Endereco
from backend.domain.enums import TipoEscola
from .base import AuditoriaEntidade



@dataclass(kw_only=True)
class Escola(AuditoriaEntidade):
    """Representa uma escola cadastrada no sistema."""

    # Identidade
    id: EscolaId | None

    # Dados principais
    inep: Inep              # Imutável
    nome: Nome
    tipo: TipoEscola        # Imutável
    municipio: Municipio    # Imutável

    # Relacionamentos
    dre_id: DreId

    # Dados opcionais
    endereco: Endereco | None = None

    # ------------------------------------------------------------------
    # Regras de negócio
    # ------------------------------------------------------------------

    def alterar_nome(self, nome: Nome) -> None:
        """Altera o nome da escola."""
        self.nome = nome
        self._marcar_tempo()

    def alterar_endereco(self, endereco: Endereco | None) -> None:
        """Altera o endereço da escola."""
        self.endereco = endereco
        self._marcar_tempo()
