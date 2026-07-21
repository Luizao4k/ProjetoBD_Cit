"""
Factory para criação de entidades TurmaCemep em testes.
"""

from __future__ import annotations

from domain.entities import TurmaCemep
from domain.value_objects import Nome
from shared.types import ResponsavelId, TurmaCemepId

from .base_factory import BaseFactory


class TurmaCemepFactory(BaseFactory):

    @classmethod
    def criar(
        cls,
        *,
        id: int | None = 1,
        nome_turma: str = "TURMA A",
        responsavel_id: int = 1,
    ) -> TurmaCemep:

        return TurmaCemep(
            id=TurmaCemepId(id) if id is not None else None,
            nome_turma=Nome(nome_turma),
            responsavel_id=ResponsavelId(responsavel_id),
        )
    