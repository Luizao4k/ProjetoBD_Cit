"""
DTOs (Data Transfer Objects) do caso de uso de Diretor.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class CriarDiretorInput:
    """
    Dados necessários para criar um novo Diretor.

    Attributes:
        escola_id:
            Identificador da escola à qual o diretor será vinculado.

        nome:
            Nome do diretor.

        telefone:
            Telefone de contato, opcional.

        email:
            E-mail de contato, opcional.
    """

    escola_id: int
    nome: str
    telefone: str | None = None
    email: str | None = None


@dataclass(frozen=True, slots=True)
class AtualizarDiretorInput:
    """
    Dados utilizados para atualizar um Diretor existente.

    A atualização é parcial. Campos com valor ``None`` indicam que
    aquele atributo não deverá ser alterado. escola_id não aparece
    aqui — trocar a escola de um diretor não é uma operação
    suportada pelo domínio.
    """

    id: int
    nome: str | None = None
    telefone: str | None = None
    email: str | None = None


@dataclass(frozen=True, slots=True)
class DiretorOutput:
    """
    Representação de saída de um Diretor.
    """

    id: int
    escola_id: int
    nome: str
    telefone: str | None
    email: str | None
    criado_em: datetime
    atualizado_em: datetime
