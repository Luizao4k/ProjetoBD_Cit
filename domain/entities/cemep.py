"""
Entidade de domínio: Cemep.
"""
from __future__ import annotations

from dataclasses import dataclass

from shared.types import EscolaId, CemepId
from .base import AuditoriaEntidade


@dataclass(kw_only=True)
class Cemep(AuditoriaEntidade):
    """
    Representa as escolas municipais com turmas cemep
    """
    id: CemepId | None

    escola_id: EscolaId
    comentario: str | None = None

    # ------------------------------------------------------------------
    # Regras de negócio
    # ------------------------------------------------------------------
    def alterar_comentario(self, comentario: str | None) -> None:
        """
        Altera o comentário do Cemep.
        A auditoria é atualizada apenas quando houver
        alteração efetiva no estado da entidade.
        """
        if self.comentario == comentario:
            return

        self.comentario = comentario
        self._marcar_tempo()
