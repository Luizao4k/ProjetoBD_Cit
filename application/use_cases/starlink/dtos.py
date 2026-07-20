"""
DTOs (Data Transfer Objects) do caso de uso de Starlink.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from domain.entities import Starlink


@dataclass(frozen=True)
class CriarStarlinkInput:
    """
    Dados necessários para criar uma nova designação de Starlink.
    """

    escola_id: int
    designacao: str


@dataclass(frozen=True)
class AtualizarStarlinkInput:
    """
    Dados para atualizar uma designação de Starlink existente.

    Atualização parcial: campos None não são alterados. escola_id
    não aparece aqui — trocar a escola de uma designação não é uma
    operação suportada pelo domínio.
    """

    id: int
    designacao: str | None = None


@dataclass(frozen=True)
class StarlinkOutput:
    """
    Representação de saída de uma designação de Starlink.
    """

    id: int
    escola_id: int
    designacao: str
    criado_em: datetime
    atualizado_em: datetime

    @classmethod
    def de_entidade(cls, starlink: Starlink) -> "StarlinkOutput":
        """
        Constrói o DTO de saída a partir da entidade de domínio.

        Levanta ValueError se a designação ainda não tiver sido
        persistida (id ainda None).
        """
        if starlink.id is None:
            raise ValueError(
                "Não é possível converter para StarlinkOutput um "
                "Starlink sem id persistido."
            )

        return cls(
            id=starlink.id,
            escola_id=starlink.escola_id,
            designacao=starlink.designacao.valor,
            criado_em=starlink.criado_em,
            atualizado_em=starlink.atualizado_em,
        )
