"""
Factory para criação de entidades Starlink em testes.
"""

from __future__ import annotations

from domain.entities import Starlink
from domain.value_objects import Nome
from shared.types import EscolaId, StarlinkId

from .base_factory import BaseFactory


class StarlinkFactory(BaseFactory):

    @classmethod
    def criar(
        cls,
        *,
        id: int | None = 1,
        designacao: str = "STARLINK ESCOLA",
        escola_id: int = 1,
    ) -> Starlink:

        return Starlink(
            id=StarlinkId(id) if id is not None else None,
            designacao=Nome(designacao),
            escola_id=EscolaId(escola_id),
        )
