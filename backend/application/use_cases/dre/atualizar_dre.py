"""
Caso de uso: atualizar uma DRE existente.
"""

from __future__ import annotations

from domain.repositories import DreRepository
from domain.value_objects import Nome, Telefone
from shared.exceptions import DreNaoEncontradaError, PersistenciaInconsistenteError
from shared.types import DreId

from .dtos import AtualizarDreInput, DreOutput


class AtualizarDreUseCase:
    """
    Atualiza uma DRE existente.

    A atualização é parcial: campos com valor ``None`` não são
    modificados.
    """

    def __init__(self, repositorio: DreRepository) -> None:
        """
        Inicializa o caso de uso.

        Args:
            repositorio:
                Repositório responsável pela persistência das DREs.
        """
        self._repositorio = repositorio

    def executar(self, dados: AtualizarDreInput) -> DreOutput:
        """
        Atualiza uma DRE existente.

        Fluxo:
            1. Converte o identificador recebido para o tipo de domínio.
            2. Busca a DRE no repositório.
            3. Lança exceção caso ela não exista.
            4. Atualiza apenas os campos informados.
            5. Persiste as alterações.
            6. Retorna um DTO com os dados atualizados.

        Args:
            dados:
                Dados necessários para a atualização.

        Returns:
            DreOutput contendo o estado atualizado da DRE.

        Raises:
            DreNaoEncontradaError:
                Caso não exista uma DRE com o id informado.
        """

        dre_id = DreId(dados.id)

        dre = self._repositorio.buscar_por_id(dre_id)

        if dre is None:
            raise DreNaoEncontradaError(dre_id)

        if dados.nome is not None:
            dre.alterar_nome(Nome(dados.nome))

        if dados.telefone is not None:
            dre.alterar_telefone(Telefone(dados.telefone))

        dre_atualizada = self._repositorio.atualizar(dre)

        if dre_atualizada.id is None:
            raise PersistenciaInconsistenteError(
                "O repositório retornou uma DRE sem id."
            )

        return DreOutput(
            id=dre_atualizada.id,
            nome=dre_atualizada.nome.valor,
            telefone=dre_atualizada.telefone.valor if dre_atualizada.telefone else None,
            criado_em=dre_atualizada.criado_em,
            atualizado_em=dre_atualizada.atualizado_em,
        )
