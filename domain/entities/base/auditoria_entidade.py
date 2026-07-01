"""
Classe base para entidades com auditoria.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass()
class AuditoriaEntidade:
    """
    Fornece campos e comportamento de auditoria para entidades do domínio.
    """

    criado_em: datetime = field(default_factory=lambda: datetime.now(UTC))
    atualizado_em: datetime = field(default_factory=lambda: datetime.now(UTC))

    def _marcar_tempo(self) -> None:
        """
        Atualiza o timestamp da última modificação da entidade.
        """
        self.atualizado_em = datetime.now(UTC)
