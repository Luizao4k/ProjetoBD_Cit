"""
Caso de uso: listar todas as Turmas do Cemep cadastradas.
"""

from __future__ import annotations

from domain.repositories import TurmaCemepRepository
from shared.exceptions import PersistenciaInconsistenteError

from .dtos import TurmaCemepOutput


class ListarTurmasCemepUseCase:
    """
    Lista todas as Turmas cadastradas.
    """

    def __init__(self, repositorio: TurmaCemepRepository) -> None:
        self._repositorio = repositorio

    def executar(self) -> list[TurmaCemepOutput]:
        """
        Lista todas as Turmas cadastradas.

        Returns:
            Lista de DTOs representando as Turmas cadastradas.

        Raises:
            PersistenciaInconsistenteError:
                Caso o repositório retorne uma entidade persistida
                em estado inconsistente.
        """

        turmas = self._repositorio.listar_todas()

        resultado: list[TurmaCemepOutput] = []

        for turma in turmas:
            if turma.id is None:
                raise PersistenciaInconsistenteError(
                    "O repositório retornou uma TurmaCemep sem id."
                )

            resultado.append(
                TurmaCemepOutput(
                    id=turma.id,
                    responsavel_id=turma.responsavel_id,
                    nome_turma=turma.nome_turma.valor,
                    criado_em=turma.criado_em,
                    atualizado_em=turma.atualizado_em,
                )
            )

        return resultado
