"""
Caso de uso: listar todas as Escolas cadastradas.
"""

from __future__ import annotations

from domain.repositories import EscolaRepository
from shared.exceptions import PersistenciaInconsistenteError

from .dtos import EscolaOutput


class ListarEscolasUseCase:
    """
    Lista todas as Escolas cadastradas.
    """

    def __init__(self, repositorio: EscolaRepository) -> None:
        self._repositorio = repositorio

    def executar(self) -> list[EscolaOutput]:
        """
        Lista todas as Escolas cadastradas.

        Returns:
            Lista de DTOs representando as Escolas cadastradas.

        Raises:
            PersistenciaInconsistenteError:
                Caso o repositório retorne uma entidade persistida
                em estado inconsistente.
        """

        escolas = self._repositorio.listar_todas()

        resultado: list[EscolaOutput] = []

        for escola in escolas:
            if escola.id is None:
                raise PersistenciaInconsistenteError(
                    "O repositório retornou uma Escola sem id."
                )

            resultado.append(
                EscolaOutput(
                    id=escola.id,
                    inep=escola.inep.valor,
                    nome=escola.nome.valor,
                    tipo=escola.tipo.value,
                    municipio=escola.municipio.valor,
                    dre_id=escola.dre_id,
                    endereco=escola.endereco.valor if escola.endereco else None,
                    criado_em=escola.criado_em,
                    atualizado_em=escola.atualizado_em,
                )
            )

        return resultado
