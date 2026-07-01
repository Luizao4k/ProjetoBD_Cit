"""
Modulo contendo atributos Escola
"""

from __future__ import annotations

from dataclasses import dataclass

from shared.types import EscolaId, DreId, DiretorId
from domain.value_objects import Inep, Nome, Municipio, Endereco
from domain.enums import TipoEscola
from .base import AuditoriaEntidade



@dataclass
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
    diretor_id: DiretorId | None = None

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

    def definir_diretor(self, diretor_id: DiretorId) -> None:
        """Define ou substitui o diretor da escola."""
        self.diretor_id = diretor_id
        self._marcar_tempo()

    def remover_diretor(self) -> None:
        """Remove o diretor da escola."""
        self.diretor_id = None
        self._marcar_tempo()
