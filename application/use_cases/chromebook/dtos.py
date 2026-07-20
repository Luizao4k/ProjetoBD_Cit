"""
DTOs (Data Transfer Objects) do caso de uso de Chromebook.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from domain.entities import Chromebook


@dataclass(frozen=True)
class CriarChromebookInput:
    """
    Dados necessários para criar um novo registro de Chromebook.
    """

    escola_id: int
    kit_aluno: int | None = None
    kit_professor: int | None = None


@dataclass(frozen=True)
class AtualizarChromebookInput:
    """
    Dados para atualizar um registro de Chromebook existente.

    Atualização parcial: campos None não são alterados.
    """

    id: int
    kit_aluno: int | None = None
    kit_professor: int | None = None


@dataclass(frozen=True)
class ChromebookOutput:
    """
    Representação de saída de um registro de Chromebook.
    """

    id: int
    escola_id: int
    kit_aluno: int | None
    kit_professor: int | None
    criado_em: datetime
    atualizado_em: datetime

    @classmethod
    def de_entidade(cls, chromebook: Chromebook) -> "ChromebookOutput":
        """
        Constrói o DTO de saída a partir da entidade de domínio.

        Levanta ValueError se o registro ainda não tiver sido
        persistido (id ainda None).
        """
        if chromebook.id is None:
            raise ValueError(
                "Não é possível converter para ChromebookOutput um "
                "Chromebook sem id persistido."
            )

        return cls(
            id=chromebook.id,
            escola_id=chromebook.escola_id,
            kit_aluno=int(chromebook.kit_aluno) if chromebook.kit_aluno else None,
            kit_professor=(
                int(chromebook.kit_professor) if chromebook.kit_professor else None
            ),
            criado_em=chromebook.criado_em,
            atualizado_em=chromebook.atualizado_em,
        )
