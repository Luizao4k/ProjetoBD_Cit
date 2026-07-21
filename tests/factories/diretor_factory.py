"""
Factory para criação de entidades Diretor em testes.
"""

from __future__ import annotations

from domain.entities import Diretor
from domain.value_objects import Nome, Telefone, Email
from shared.types import DiretorId, EscolaId

from .base_factory import BaseFactory


class DiretorFactory(BaseFactory):
    """
    Factory responsável por criar entidades Diretor válidas.
    """

    @classmethod
    def criar(
        cls,
        *,
        id: int | None = 1,
        escola_id: int = 1,
        nome: str = "JOÃO DA SILVA",
        telefone: str | None = "91999999999",
        email: str | None = "joao@email.com",
    ) -> Diretor:

        return Diretor(
            id=DiretorId(id) if id is not None else None,
            escola_id=EscolaId(escola_id),
            nome=Nome(nome),
            telefone=Telefone(telefone) if telefone is not None else None,
            email=Email(email) if email is not None else None,
        )
