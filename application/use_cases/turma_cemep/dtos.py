"""
DTOs (Data Transfer Objects) do caso de uso de TurmaCemep.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from domain.entities import TurmaCemep


@dataclass(frozen=True)
class CriarTurmaCemepInput:
    """
    Dados necessários para criar uma nova Turma do Cemep.
    """

    responsavel_id: int
    nome_turma: str


@dataclass(frozen=True)
class AtualizarTurmaCemepInput:
    """
    Dados para atualizar uma Turma existente.

    Atualização parcial: campos None não são alterados.
    responsavel_id não aparece aqui — trocar o responsável de uma
    turma não é uma operação suportada pelo domínio.
    """

    id: int
    nome_turma: str | None = None


@dataclass(frozen=True)
class TurmaCemepOutput:
    """
    Representação de saída de uma Turma do Cemep.
    """

    id: int
    responsavel_id: int
    nome_turma: str
    criado_em: datetime
    atualizado_em: datetime

    @classmethod
    def de_entidade(cls, turma: TurmaCemep) -> "TurmaCemepOutput":
        """
        Constrói o DTO de saída a partir da entidade de domínio.

        Levanta ValueError se a Turma ainda não tiver sido
        persistida (id ainda None).
        """
        if turma.id is None:
            raise ValueError(
                "Não é possível converter para TurmaCemepOutput "
                "uma TurmaCemep sem id persistido."
            )

        return cls(
            id=turma.id,
            responsavel_id=turma.responsavel_id,
            nome_turma=turma.nome_turma.valor,
            criado_em=turma.criado_em,
            atualizado_em=turma.atualizado_em,
        )
