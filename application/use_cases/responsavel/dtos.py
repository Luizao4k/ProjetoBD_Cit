"""
DTOs (Data Transfer Objects) do caso de uso de Responsavel.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from domain.entities import Responsavel


@dataclass(frozen=True)
class CriarResponsavelInput:
    """
    Dados necessários para criar um novo Responsável.
    """

    cemep_id: int
    nome: str


@dataclass(frozen=True)
class AtualizarResponsavelInput:
    """
    Dados para atualizar um Responsável existente.

    Atualização parcial: campos None não são alterados. cemep_id
    não aparece aqui — trocar o Cemep de um responsável não é uma
    operação suportada pelo domínio.
    """

    id: int
    nome: str | None = None


@dataclass(frozen=True)
class ResponsavelOutput:
    """
    Representação de saída de um Responsável.
    """

    id: int
    cemep_id: int
    nome: str
    criado_em: datetime
    atualizado_em: datetime

    @classmethod
    def de_entidade(cls, responsavel: Responsavel) -> "ResponsavelOutput":
        """
        Constrói o DTO de saída a partir da entidade de domínio.

        Levanta ValueError se o Responsável ainda não tiver sido
        persistido (id ainda None).
        """
        if responsavel.id is None:
            raise ValueError(
                "Não é possível converter para ResponsavelOutput um "
                "Responsavel sem id persistido."
            )

        return cls(
            id=responsavel.id,
            cemep_id=responsavel.cemep_id,
            nome=responsavel.nome.valor,
            criado_em=responsavel.criado_em,
            atualizado_em=responsavel.atualizado_em,
        )
