"""
Caso de uso: listar as Escolas de uma DRE (relação 1:N).
"""

from __future__ import annotations

from domain.repositories import EscolaRepository
from shared.exceptions import PersistenciaInconsistenteError
from shared.types import DreId

from .dtos import EscolaOutput


class BuscarEscolasPorDreUseCase:
    """
    Retorna todas as Escolas vinculadas a uma DRE.

    Diferente das relações 1:1 (ex: Diretor, Cemep), aqui uma
    lista vazia é um resultado legítimo (a DRE simplesmente ainda
    não tem escolas cadastradas) — por isso não há exceção
    equivalente a "EscolaNaoPossuiCemepError" neste caso.
    """

    def __init__(self, repositorio: EscolaRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dre_id: int) -> list[EscolaOutput]:
        """
        Lista as Escolas de uma DRE.

        Args:
            dre_id:
                Identificador da DRE.

        Returns:
            Lista de DTOs representando as Escolas da DRE. Pode
            ser vazia.

        Raises:
            PersistenciaInconsistenteError:
                Caso o repositório retorne uma entidade persistida
                em estado inconsistente.
        """

        id_dre = DreId(dre_id)

        escolas = self._repositorio.buscar_por_dre(id_dre)

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
