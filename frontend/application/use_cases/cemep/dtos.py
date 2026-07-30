"""
DTOs (Data Transfer Objects) do caso de uso de Cemep.

Os DTOs pertencem à camada de aplicação e são responsáveis apenas
por transportar dados entre quem invoca o caso de uso (API, CLI,
interface gráfica, testes, etc.) e o próprio caso de uso.

Eles utilizam apenas tipos primitivos e não possuem regras de negócio.
A conversão entre Entidades e DTOs é responsabilidade do Use Case,
mantendo o DTO desacoplado do domínio.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class CriarCemepInput:
    """
    Dados necessários para criar um novo Cemep.

    Attributes:
        escola_id:
            Identificador da escola onde o Cemep será criado.

        comentario:
            Comentário opcional associado ao Cemep.
    """

    escola_id: int
    comentario: str | None = None


@dataclass(frozen=True, slots=True)
class AtualizarCemepInput:
    """
    Dados utilizados para atualizar um Cemep existente.

    A atualização é parcial. Campos com valor ``None`` indicam que
    aquele atributo não deverá ser alterado.

    Observação:
        Atualmente não existe uma forma de limpar explicitamente o
        comentário (defini-lo como vazio) através deste DTO.
    """

    id: int
    comentario: str | None = None


@dataclass(frozen=True, slots=True)
class CemepOutput:
    """
    Representação de saída de um Cemep.

    Este DTO é utilizado para devolver informações ao consumidor
    do caso de uso (API, interface gráfica, testes etc.).

    Todos os atributos utilizam tipos primitivos para evitar
    dependência da camada de domínio.
    """

    id: int
    escola_id: int
    comentario: str | None
    criado_em: datetime
    atualizado_em: datetime
