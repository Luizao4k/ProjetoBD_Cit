"""
DTOs (Data Transfer Objects) do caso de uso de Diretor.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from domain.entities import Diretor


@dataclass(frozen=True)
class CriarDiretorInput:
    """
    Dados necessários para criar um novo Diretor.
    """

    escola_id: int
    nome: str
    telefone: str | None = None
    email: str | None = None


@dataclass(frozen=True)
class AtualizarDiretorInput:
    """
    Dados para atualizar um Diretor existente.

    Atualização parcial: campos None não são alterados. escola_id
    não aparece aqui — trocar a escola de um diretor não é uma
    operação suportada pelo domínio (a entidade não possui
    alterar_escola); isso seria remover o diretor e criar outro.
    """

    id: int
    nome: str | None = None
    telefone: str | None = None
    email: str | None = None


@dataclass(frozen=True)
class DiretorOutput:
    """
    Representação de saída de um Diretor, já com os valores
    "desembrulhados" dos Value Objects.
    """

    id: int
    escola_id: int
    nome: str
    telefone: str | None
    email: str | None
    criado_em: datetime
    atualizado_em: datetime

    @classmethod
    def de_entidade(cls, diretor: Diretor) -> "DiretorOutput":
        """
        Constrói o DTO de saída a partir da entidade de domínio.

        Levanta ValueError se o Diretor ainda não tiver sido
        persistido (id ainda None).
        """
        if diretor.id is None:
            raise ValueError(
                "Não é possível converter para DiretorOutput um "
                "Diretor sem id persistido."
            )

        return cls(
            id=diretor.id,
            escola_id=diretor.escola_id,
            nome=diretor.nome.valor,
            telefone=diretor.telefone.valor if diretor.telefone else None,
            email=diretor.email.valor if diretor.email else None,
            criado_em=diretor.criado_em,
            atualizado_em=diretor.atualizado_em,
        )
