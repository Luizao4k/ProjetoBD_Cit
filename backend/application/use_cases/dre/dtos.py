"""
DTOs (Data Transfer Objects) do caso de uso de DRE.

Os DTOs pertencem à camada de aplicação e são responsáveis apenas
por transportar dados entre quem invoca o caso de uso (API, CLI,
interface gráfica, testes etc.) e o próprio caso de uso.

Eles utilizam apenas tipos primitivos e não possuem regras de negócio.
A conversão entre Entidades e DTOs é responsabilidade do Use Case,
mantendo o DTO desacoplado do domínio.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class CriarDreInput:
    """
    Dados necessários para criar uma nova DRE.

    Attributes:
        nome:
            Nome da DRE.

        telefone:
            Telefone de contato, opcional.
    """

    nome: str
    telefone: str | None = None


@dataclass(frozen=True, slots=True)
class AtualizarDreInput:
    """
    Dados utilizados para atualizar uma DRE existente.

    A atualização é parcial. Campos com valor ``None`` indicam que
    aquele atributo não deverá ser alterado.

    Observação:
        Atualmente não existe uma forma de limpar explicitamente o
        telefone (defini-lo como vazio) através deste DTO.
    """

    id: int
    nome: str | None = None
    telefone: str | None = None


@dataclass(frozen=True, slots=True)
class DreOutput:
    """
    Representação de saída de uma DRE.

    Este DTO é utilizado para devolver informações ao consumidor
    do caso de uso (API, interface gráfica, testes etc.).

    Todos os atributos utilizam tipos primitivos para evitar
    dependência da camada de domínio.
    """

    id: int
    nome: str
    telefone: str | None
    criado_em: datetime
    atualizado_em: datetime
