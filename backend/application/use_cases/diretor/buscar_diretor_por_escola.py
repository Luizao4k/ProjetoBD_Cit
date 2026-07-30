"""
Caso de uso: buscar o Diretor de uma Escola (relação 1:1).
"""

from __future__ import annotations

from domain.repositories import DiretorRepository
from shared.exceptions import (
    EscolaNaoPossuiDiretorError,
    PersistenciaInconsistenteError,
)
from shared.types import EscolaId

from .dtos import DiretorOutput


class BuscarDiretorPorEscolaUseCase:
    """
    Retorna o Diretor vinculado à escola informada.

    Raises:
        EscolaNaoPossuiDiretorError:
            Caso a escola não possua um diretor cadastrado.
    """

    def __init__(self, repositorio: DiretorRepository) -> None:
        self._repositorio = repositorio

    def executar(self, escola_id: int) -> DiretorOutput:
        """
        Busca o Diretor associado à escola informada.

        Args:
            escola_id:
                Identificador da escola.

        Returns:
            DTO contendo os dados do Diretor.

        Raises:
            EscolaNaoPossuiDiretorError:
                Caso não exista um diretor vinculado à escola.
        """

        id_escola = EscolaId(escola_id)

        diretor = self._repositorio.buscar_por_escola(id_escola)

        if diretor is None:
            raise EscolaNaoPossuiDiretorError(id_escola)

        if diretor.id is None:
            raise PersistenciaInconsistenteError(
                "O repositório retornou um Diretor sem id."
            )

        return DiretorOutput(
            id=diretor.id,
            escola_id=diretor.escola_id,
            nome=diretor.nome.valor,
            telefone=diretor.telefone.valor if diretor.telefone else None,
            email=diretor.email.valor if diretor.email else None,
            criado_em=diretor.criado_em,
            atualizado_em=diretor.atualizado_em,
        )
