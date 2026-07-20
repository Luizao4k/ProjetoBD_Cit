"""
DTOs (Data Transfer Objects) do caso de uso de Escola.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from domain.entities import Escola


@dataclass(frozen=True)
class CriarEscolaInput:
    """
    Dados necessários para criar uma nova Escola.
    """

    inep: str
    nome: str
    tipo: str
    municipio: str
    dre_id: int
    endereco: str | None = None


@dataclass(frozen=True)
class AtualizarEscolaInput:
    """
    Dados para atualizar uma Escola existente.

    Atualização parcial: campos None não são alterados. inep, tipo
    e municipio não aparecem aqui porque são imutáveis no domínio
    (a entidade Escola não possui alterar_inep/alterar_tipo/
    alterar_municipio).
    """

    id: int
    nome: str | None = None
    endereco: str | None = None


@dataclass(frozen=True)
class EscolaOutput:
    """
    Representação de saída de uma Escola, já com os valores
    "desembrulhados" dos Value Objects.
    """

    id: int
    inep: str
    nome: str
    tipo: str
    municipio: str
    dre_id: int
    endereco: str | None
    criado_em: datetime
    atualizado_em: datetime

    @classmethod
    def de_entidade(cls, escola: Escola) -> "EscolaOutput":
        """
        Constrói o DTO de saída a partir da entidade de domínio.

        Levanta ValueError se a Escola ainda não tiver sido
        persistida (id ainda None).
        """
        if escola.id is None:
            raise ValueError(
                "Não é possível converter para EscolaOutput uma "
                "Escola sem id persistido."
            )

        return cls(
            id=escola.id,
            inep=escola.inep.valor,
            nome=escola.nome.valor,
            tipo=escola.tipo.value,
            municipio=escola.municipio.valor,
            dre_id=escola.dre_id,
            endereco=escola.endereco.valor if escola.endereco else None,
            criado_em=escola.criado_em,
            atualizado_em=escola.atualizado_em,
        )
