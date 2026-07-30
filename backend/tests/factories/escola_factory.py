"""
Factory para criação de entidades Escola em testes.
"""

from __future__ import annotations

from domain.entities import Escola
from domain.enums import TipoEscola
from domain.value_objects import Endereco, Inep, Municipio, Nome
from shared.types import DreId, EscolaId

from .base_factory import BaseFactory


class EscolaFactory(BaseFactory):
    """
    Factory responsável por criar entidades Escola válidas.
    """

    @classmethod
    def criar(
        cls,
        *,
        id: int | None = 1,
        inep: str = "15000000",
        nome: str = "ESCOLA TESTE",
        tipo: TipoEscola = TipoEscola.ESTADUAL,
        municipio: str = "BELÉM",
        dre_id: int = 1,
        endereco: str | None = None,
    ) -> Escola:

        return Escola(
            id=EscolaId(id) if id is not None else None,
            inep=Inep(inep),
            nome=Nome(nome),
            tipo=tipo,
            municipio=Municipio(municipio),
            dre_id=DreId(dre_id),
            endereco=Endereco(endereco) if endereco is not None else None,
        )
