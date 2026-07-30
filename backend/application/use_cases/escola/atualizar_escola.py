"""
Caso de uso: atualizar uma Escola existente.
"""

from __future__ import annotations

from domain.repositories import EscolaRepository
from domain.value_objects import Endereco, Nome
from shared.exceptions import (
    EscolaNaoEncontradaError,
    PersistenciaInconsistenteError,
)
from shared.types import EscolaId

from .dtos import AtualizarEscolaInput, EscolaOutput


class AtualizarEscolaUseCase:
    """
    Atualiza uma Escola existente.

    A atualização é parcial: campos com valor ``None`` não são
    modificados. inep, tipo e municipio não podem ser alterados
    (são imutáveis no domínio).
    """

    def __init__(self, repositorio: EscolaRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dados: AtualizarEscolaInput) -> EscolaOutput:
        """
        Atualiza uma Escola existente.

        Args:
            dados:
                Dados necessários para a atualização.

        Returns:
            EscolaOutput contendo o estado atualizado da Escola.

        Raises:
            EscolaNaoEncontradaError:
                Caso não exista uma Escola com o id informado.
        """

        escola_id = EscolaId(dados.id)

        escola = self._repositorio.buscar_por_id(escola_id)

        if escola is None:
            raise EscolaNaoEncontradaError(escola_id)

        if dados.nome is not None:
            escola.alterar_nome(Nome(dados.nome))

        if dados.endereco is not None:
            escola.alterar_endereco(Endereco(dados.endereco))

        escola_atualizada = self._repositorio.atualizar(escola)

        if escola_atualizada.id is None:
            raise PersistenciaInconsistenteError(
                "O repositório retornou uma Escola sem id."
            )

        return EscolaOutput(
            id=escola_atualizada.id,
            inep=escola_atualizada.inep.valor,
            nome=escola_atualizada.nome.valor,
            tipo=escola_atualizada.tipo.value,
            municipio=escola_atualizada.municipio.valor,
            dre_id=escola_atualizada.dre_id,
            endereco=escola_atualizada.endereco.valor if escola_atualizada.endereco else None,
            criado_em=escola_atualizada.criado_em,
            atualizado_em=escola_atualizada.atualizado_em,
        )
