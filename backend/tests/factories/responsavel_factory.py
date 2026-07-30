"""
Factory para criação de entidades Responsavel em testes.
"""

from __future__ import annotations

from domain.entities import Responsavel
from domain.value_objects import Nome
from shared.types import ResponsavelId, CemepId

from .base_factory import BaseFactory


class ResponsavelFactory(BaseFactory):
    """
    Factory responsável por criar entidades Responsavel válidas.
    """

    @classmethod
    def criar(
        cls,
        *,
        id: int | None = 1,
        nome: str = "JOÃO RESPONSÁVEL",
        cemep_id: int = 1,
    ) -> Responsavel:

        return Responsavel(
            id=ResponsavelId(id) if id is not None else None,
            nome=Nome(nome),
            cemep_id=CemepId(cemep_id),
        )
