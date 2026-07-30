"""
Caso de uso: listar todas as DREs cadastradas.
"""

from __future__ import annotations

from domain.repositories import DreRepository
from shared.exceptions import PersistenciaInconsistenteError

from .dtos import DreOutput


class ListarDresUseCase:
    """
    Lista todas as DREs cadastradas.

    Os dados retornados são convertidos para DTOs, ficando
    prontos para consumo por APIs, interfaces gráficas ou
    exportação em planilha.
    """

    def __init__(self, repositorio: DreRepository) -> None:
        """
        Inicializa o caso de uso.

        Args:
            repositorio:
                Repositório responsável pela persistência das DREs.
        """
        self._repositorio = repositorio

    def executar(self) -> list[DreOutput]:
        """
        Lista todas as DREs cadastradas.

        Returns:
            Lista de DTOs representando as DREs cadastradas.

        Raises:
            PersistenciaInconsistenteError:
                Caso o repositório retorne uma entidade persistida
                em estado inconsistente.
        """

        dres = self._repositorio.listar_todas()

        resultado: list[DreOutput] = []

        for dre in dres:
            if dre.id is None:
                raise PersistenciaInconsistenteError(
                    "O repositório retornou uma DRE sem id."
                )

            resultado.append(
                DreOutput(
                    id=dre.id,
                    nome=dre.nome.valor,
                    telefone=dre.telefone.valor if dre.telefone else None,
                    criado_em=dre.criado_em,
                    atualizado_em=dre.atualizado_em,
                )
            )

        return resultado
