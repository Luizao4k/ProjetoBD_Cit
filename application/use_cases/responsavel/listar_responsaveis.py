"""
Caso de uso: listar todos os Responsáveis cadastrados.
"""

from __future__ import annotations

from domain.repositories import ResponsavelRepository
from shared.exceptions import PersistenciaInconsistenteError

from .dtos import ResponsavelOutput


class ListarResponsaveisUseCase:
    """
    Lista todos os Responsáveis cadastrados.
    """

    def __init__(self, repositorio: ResponsavelRepository) -> None:
        self._repositorio = repositorio

    def executar(self) -> list[ResponsavelOutput]:
        """
        Lista todos os Responsáveis cadastrados.

        Returns:
            Lista de DTOs representando os Responsáveis cadastrados.

        Raises:
            PersistenciaInconsistenteError:
                Caso o repositório retorne uma entidade persistida
                em estado inconsistente.
        """

        responsaveis = self._repositorio.listar_todas()

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
