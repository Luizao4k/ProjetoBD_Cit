"""Factory para cemep"""
from domain.entities import Cemep
from shared.types import CemepId, EscolaId
from tests.factories.base_factory import BaseFactory


class CemepFactory(BaseFactory):

    @classmethod
    def criar(
        cls,
        *,
        id: int | None = 1,
        escola_id: int = 1,
        comentario: str | None = "Comentário teste",
    ) -> Cemep:

        return Cemep(
            id=CemepId(id) if id is not None else None,
            escola_id=EscolaId(escola_id),
            comentario=comentario,
        )
