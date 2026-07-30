"""
Caso de uso: buscar o Cemep de uma Escola (relação 1:1).
"""

from __future__ import annotations

from domain.repositories import CemepRepository
from shared.exceptions import EscolaNaoPossuiCemepError, PersistenciaInconsistenteError
from shared.types import EscolaId

from .dtos import CemepOutput


class BuscarCemepPorEscolaUseCase:
    """
    Retorna o Cemep vinculado à escola informada.

    Raises:
        EscolaNaoPossuiCemepError:
            Caso a escola não possua um Cemep cadastrado.
    """

    def __init__(self, repositorio: CemepRepository) -> None:
        self._repositorio = repositorio

    def executar(self, escola_id: int) -> CemepOutput:
        """
        Busca o Cemep associado à escola informada.

        Args:
            escola_id:
                Identificador da escola.

        Returns:
            DTO contendo os dados do Cemep.

        Raises:
            EscolaNaoPossuiCemepError:
                Caso não exista um Cemep vinculado à escola.
        """

        id_escola = EscolaId(escola_id)

        cemep = self._repositorio.buscar_por_escola(id_escola)

        if cemep is None:
            raise EscolaNaoPossuiCemepError(id_escola)

        if cemep.id is None:
            raise PersistenciaInconsistenteError(
                "O repositório retornou um Cemep sem id."
            )

        return CemepOutput(
            id=cemep.id,
            escola_id=cemep.escola_id,
            comentario=cemep.comentario.valor if cemep.comentario else None,
            criado_em=cemep.criado_em,
            atualizado_em=cemep.atualizado_em,
        )