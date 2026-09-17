"""
Caso de uso: listar todas as Escolas cadastradas.
"""

from __future__ import annotations

from domain.repositories import EscolaRepository, DreRepository
from shared.exceptions import PersistenciaInconsistenteError

from .dtos import EscolaOutput
from ..dre.dtos import DreOutput


class ListarEscolasUseCase:
    """
    Lista todas as Escolas cadastradas.
    """

    def __init__(self, repositorio: EscolaRepository,  dre_repositorio: DreRepository) -> None:
        self._repositorio = repositorio
        self._dre_repositorio = dre_repositorio

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

         # Otimização simples para não buscar a mesma DRE várias vezes no laço
        dres_carregadas = {}
        resultado = []

        resultado: list[EscolaOutput] = []

        for escola in escolas:
            if escola.id is None:
                raise PersistenciaInconsistenteError(
                    "O repositório retornou uma Escola sem id."
                )

        #Busca e popula a DRE da escola atual
            dre_output = None
            if escola.dre_id:
                if escola.dre_id not in dres_carregadas:
                    dre = self._dre_repositorio.buscar_por_id(escola.dre_id)
                    if dre:
                        dre_id = dre.id
                        if dre_id is None:
                            raise PersistenciaInconsistenteError(
                                "O repositório retornou uma DRE sem id."
                            )
                        dres_carregadas[escola.dre_id] = DreOutput(
                            id=dre_id,
                            nome=dre.nome.valor,
                            telefone=dre.telefone.valor if dre.telefone else None,
                            criado_em=dre.criado_em,
                            atualizado_em=dre.atualizado_em,
                        )
                dre_output = dres_carregadas.get(escola.dre_id)

            resultado.append(
                EscolaOutput(
                    id=escola.id,
                    inep=escola.inep.valor,
                    nome=escola.nome.valor,
                    tipo=escola.tipo.value,
                    municipio=escola.municipio.valor,
                    dre_id=escola.dre_id,
                    dre=dre_output,
                    endereco=escola.endereco.valor if escola.endereco else None,
                    criado_em=escola.criado_em,
                    atualizado_em=escola.atualizado_em,
                )
            )

        return resultado
