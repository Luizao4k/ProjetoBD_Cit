"""
Factory para criação de entidades Dre em testes.
"""

from __future__ import annotations

from domain.entities import Dre
from domain.value_objects import Nome, Telefone
from shared.types import DreId

from .base_factory import BaseFactory


class DreFactory(BaseFactory):
    """
    Factory responsável por criar entidades Dre válidas.
    """

    @classmethod
    def criar(
        cls,
        *,
        id: int | None = 1,
        nome: str = "DRE BELÉM",
        telefone: str | None = "91999999999",
    ) -> Dre:

        return Dre(
            id=DreId(id) if id is not None else None,
            nome=Nome(nome),
            telefone=Telefone(telefone) if telefone is not None else None,
        )
