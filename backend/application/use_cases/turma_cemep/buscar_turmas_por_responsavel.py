"""
Caso de uso: listar as Turmas de um Responsável (relação 1:N).
"""

from __future__ import annotations

from domain.repositories import TurmaCemepRepository
from shared.exceptions import PersistenciaInconsistenteError
from shared.types import ResponsavelId

from .dtos import TurmaCemepOutput


class BuscarTurmasPorResponsavelUseCase:
    """
    Retorna todas as Turmas vinculadas a um Responsável.

    Como se trata de uma relação 1:N, uma lista vazia é um
    resultado legítimo — não há exceção equivalente à das
    relações 1:1.
    """

    def __init__(self, repositorio: TurmaCemepRepository) -> None:
        self._repositorio = repositorio

    def executar(self, responsavel_id: int) -> list[TurmaCemepOutput]:
        """
        Lista as Turmas de um Responsável.

        Args:
            responsavel_id:
                Identificador do Responsável.

        Returns:
            Lista de DTOs representando as Turmas do responsável.
            Pode ser vazia.

        Raises:
            PersistenciaInconsistenteError:
                Caso o repositório retorne uma entidade persistida
                em estado inconsistente.
        """

        id_responsavel = ResponsavelId(responsavel_id)

        turmas = self._repositorio.buscar_por_responsavel(id_responsavel)

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
