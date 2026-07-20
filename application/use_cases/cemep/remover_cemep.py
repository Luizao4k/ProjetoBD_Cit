"""
Caso de uso: remover um Cemep existente.
"""

from __future__ import annotations

from domain.repositories import CemepRepository
from shared.exceptions import CemepNaoEncontradoError
from shared.types import CemepId


class RemoverCemepUseCase:
    """
    Remove um Cemep existente.

    Caso o identificador informado não corresponda a um
    Cemep cadastrado, uma exceção é lançada.
    """

    def __init__(self, repositorio: CemepRepository) -> None:
        """
        Inicializa o caso de uso.

        Args:
            repositorio:
                Repositório responsável pela persistência dos Cemeps.
        """
        self._repositorio = repositorio

    def executar(self, cemep_id: int) -> None:
        """
        Remove um Cemep.

        Args:
            cemep_id:
                Identificador do Cemep.

        Raises:
            CemepNaoEncontradoError:
                Caso não exista um Cemep com o identificador informado.
        """

        # Converte o identificador recebido para o tipo do domínio.
        cemep_id = CemepId(cemep_id)

        # Verifica se o Cemep existe antes de removê-lo.
        cemep = self._repositorio.buscar_por_id(cemep_id)

        if cemep is None:
            raise CemepNaoEncontradoError(cemep_id)

        # Remove o Cemep da persistência.
        self._repositorio.remover(cemep_id)
