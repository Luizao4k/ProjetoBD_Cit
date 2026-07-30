"""
Caso de uso: listar todos os Diretores cadastrados.
"""

from __future__ import annotations

from domain.repositories import DiretorRepository
from shared.exceptions import PersistenciaInconsistenteError

from .dtos import DiretorOutput


class ListarDiretoresUseCase:
    """
    Lista todos os Diretores cadastrados.
    """

    def __init__(self, repositorio: DiretorRepository) -> None:
        self._repositorio = repositorio

    def executar(self) -> list[DiretorOutput]:
        """
        Lista todos os Diretores cadastrados.

        Returns:
            Lista de DTOs representando os Diretores cadastrados.

        Raises:
            PersistenciaInconsistenteError:
                Caso o repositório retorne uma entidade persistida
                em estado inconsistente.
        """

        diretores = self._repositorio.listar_todas()

        resultado: list[DiretorOutput] = []

        for diretor in diretores:
            if diretor.id is None:
                raise PersistenciaInconsistenteError(
                    "O repositório retornou um Diretor sem id."
                )

            resultado.append(
                DiretorOutput(
                    id=diretor.id,
                    escola_id=diretor.escola_id,
                    nome=diretor.nome.valor,
                    telefone=diretor.telefone.valor if diretor.telefone else None,
                    email=diretor.email.valor if diretor.email else None,
                    criado_em=diretor.criado_em,
                    atualizado_em=diretor.atualizado_em,
                )
            )

        return resultado
