"""
Factory para criação de entidades Chromebook em testes.
"""

from __future__ import annotations

from domain.entities import Chromebook
from domain.value_objects import Quantidade
from shared.types import ChromebooksId, EscolaId

from .base_factory import BaseFactory


class ChromebookFactory(BaseFactory):

    @classmethod
    def criar(
        cls,
        *,
        id: int | None = 1,
        escola_id: int = 1,
        kit_aluno: int | None = 30,
        kit_professor: int | None = 2,
    ) -> Chromebook:

        return Chromebook(
            id=ChromebooksId(id) if id is not None else None,
            escola_id=EscolaId(escola_id),
            kit_aluno=Quantidade(kit_aluno) if kit_aluno is not None else None,
            kit_professor=Quantidade(kit_professor) if kit_professor is not None else None,
        )
