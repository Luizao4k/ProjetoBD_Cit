"""
Caso de uso: listar os Responsáveis de um Cemep (relação 1:N).
"""

from __future__ import annotations

from domain.repositories import ResponsavelRepository
from shared.exceptions import PersistenciaInconsistenteError
from shared.types import CemepId

from .dtos import ResponsavelOutput


class BuscarResponsaveisPorCemepUseCase:
    """
    Retorna todos os Responsáveis vinculados a um Cemep.

    Como se trata de uma relação 1:N, uma lista vazia é um
    resultado legítimo (o Cemep ainda não tem responsáveis
    cadastrados) — não há exceção equivalente à das relações 1:1.
    """

    def __init__(self, repositorio: ResponsavelRepository) -> None:
        self._repositorio = repositorio

    def executar(self, cemep_id: int) -> list[ResponsavelOutput]:
        """
        Lista os Responsáveis de um Cemep.

        Args:
            cemep_id:
                Identificador do Cemep.

        Returns:
            Lista de DTOs representando os Responsáveis do Cemep.
            Pode ser vazia.

        Raises:
            PersistenciaInconsistenteError:
                Caso o repositório retorne uma entidade persistida
                em estado inconsistente.
        """

        id_cemep = CemepId(cemep_id)

        responsaveis = self._repositorio.buscar_por_cemep(id_cemep)

        resultado: list[ResponsavelOutput] = []

        for responsavel in responsaveis:
            if responsavel.id is None:
                raise PersistenciaInconsistenteError(
                    "O repositório retornou um Responsavel sem id."
                )

            resultado.append(
                ResponsavelOutput(
                    id=responsavel.id,
                    cemep_id=responsavel.cemep_id,
                    nome=responsavel.nome.valor,
                    criado_em=responsavel.criado_em,
                    atualizado_em=responsavel.atualizado_em,
                )
            )

        return resultado
