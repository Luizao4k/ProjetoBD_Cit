"""
DTOs (Data Transfer Objects) do caso de uso de DRE.

Servem para desacoplar quem chama o caso de uso dos Value Objects de
domínio: a entrada e a saída trabalham só com tipos primitivos
(str, int, datetime), o que facilita tanto a integração com uma API/UI
quanto a futura exportação para planilha.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

from domain.entities import Dre


@dataclass(frozen=True)
class CriarDreInput:
    """
    Dados necessários para criar uma nova DRE.
    """

    nome: str
    telefone: str | None = None


@dataclass(frozen=True)
class AtualizarDreInput:
    """
    Dados para atualizar uma DRE existente.

    Atualização parcial: campos deixados como None não são alterados.
    Não há, hoje, uma forma de limpar explicitamente o telefone
    (setá-lo como None) através deste DTO — se essa necessidade
    surgir, será preciso um valor sentinela para diferenciar
    "não informado" de "definir como vazio".
    """

    id: int
    nome: str | None = None
    telefone: str | None = None


@dataclass(frozen=True)
class DreOutput:
    """
    Representação de saída de uma DRE, já com os valores
    "desembrulhados" dos Value Objects.
    """

    id: int
    nome: str
    telefone: str | None
    criado_em: datetime
    atualizado_em: datetime

    @classmethod
    def de_entidade(cls, dre: Dre) -> "DreOutput":
        """
        Constrói o DTO de saída a partir da entidade de domínio.
        """
        return cls(
            id=dre.id,
            nome=dre.nome.valor,
            telefone=dre.telefone.valor if dre.telefone else None,
            criado_em=dre.criado_em,
            atualizado_em=dre.atualizado_em,
        )
