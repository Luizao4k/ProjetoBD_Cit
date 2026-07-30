"""
Caso de uso: atualizar um Cemep existente.
"""

from __future__ import annotations

from domain.repositories import CemepRepository
from domain.value_objects import Comentario
from shared.exceptions import CemepNaoEncontradoError, PersistenciaInconsistenteError
from shared.types import CemepId

from .dtos import AtualizarCemepInput, CemepOutput

class AtualizarCemepUseCase:
    """
    Atualiza um Cemep existente.

    A atualização é parcial: campos com valor ``None`` não são
    modificados.
    """

    def __init__(self, repositorio: CemepRepository) -> None:
        """
        Inicializa o caso de uso.

        Args:
            repositorio:
                Repositório responsável pela persistência dos Cemep.
        """
        self._repositorio = repositorio

    def executar(self, dados: AtualizarCemepInput) -> CemepOutput:
        """
        Atualiza um Cemep existente.

        Fluxo:
            1. Converte o identificador recebido para o tipo de domínio.
            2. Busca o Cemep no repositório.
            3. Lança exceção caso ele não exista.
            4. Atualiza apenas os campos informados.
            5. Persiste as alterações.
            6. Retorna um DTO com os dados atualizados.

        Args:
            dados:
                Dados necessários para a atualização.

        Returns:
            CemepOutput contendo o estado atualizado do Cemep.

        Raises:
            CemepNaoEncontradoError:
                Caso não exista um Cemep com o id informado.
        """

        # Converte o id primitivo recebido pelo DTO para o tipo do domínio.
        cemep_id = CemepId(dados.id)

        # Recupera o Cemep persistido.
        cemep = self._repositorio.buscar_por_id(cemep_id)

        # Impede atualização de um registro inexistente.
        if cemep is None:
            raise CemepNaoEncontradoError(cemep_id)

        # Atualiza apenas os campos informados.
        if dados.comentario is not None:
            cemep.alterar_comentario(Comentario(dados.comentario))

        # Persiste as alterações.
        cemep_atualizado = self._repositorio.atualizar(cemep)

        if cemep_atualizado.id is None:
            raise PersistenciaInconsistenteError(
            "O repositório retornou um Cemep sem id.")

        # Converte a entidade de domínio para o DTO de saída.
        return CemepOutput(
            id=cemep_atualizado.id,
            escola_id=cemep_atualizado.escola_id,
            comentario=cemep_atualizado.comentario.valor if cemep_atualizado.comentario else None,
            criado_em=cemep_atualizado.criado_em,
            atualizado_em=cemep_atualizado.atualizado_em,
        )
