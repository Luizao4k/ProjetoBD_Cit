"""
Caso de uso: criar uma nova Escola.
"""

from __future__ import annotations

from domain.entities import Escola
from domain.enums import TipoEscola
from domain.repositories import EscolaRepository
from domain.value_objects import Endereco, Inep, Municipio, Nome
from shared.exceptions import PersistenciaInconsistenteError
from shared.types import DreId

from .dtos import CriarEscolaInput, EscolaOutput


class CriarEscolaUseCase:
    """
    Cria uma nova Escola.
    """

    def __init__(self, repositorio: EscolaRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dados: CriarEscolaInput) -> EscolaOutput:
        """
        Cria uma nova Escola.

        Args:
            dados:
                Dados necessários para a criação da Escola.

        Returns:
            DTO contendo os dados da Escola criada.

        Raises:
            ValueError:
                Caso `dados.tipo` não corresponda a um TipoEscola
                válido (ESTADUAL ou MUNICIPAL).

            PersistenciaInconsistenteError:
                Caso o repositório retorne uma entidade persistida
                em estado inconsistente.
        """

        escola = Escola(
            id=None,
            inep=Inep(dados.inep),
            nome=Nome(dados.nome),
            tipo=TipoEscola(dados.tipo),
            municipio=Municipio(dados.municipio),
            dre_id=DreId(dados.dre_id),
            endereco=Endereco(dados.endereco) if dados.endereco else None,
        )

        escola_criada = self._repositorio.salvar(escola)

        if escola_criada.id is None:
            raise PersistenciaInconsistenteError(
                "O repositório retornou uma Escola sem id."
            )

        return EscolaOutput(
            id=escola_criada.id,
            inep=escola_criada.inep.valor,
            nome=escola_criada.nome.valor,
            tipo=escola_criada.tipo.value,
            municipio=escola_criada.municipio.valor,
            dre_id=escola_criada.dre_id,
            endereco=escola_criada.endereco.valor if escola_criada.endereco else None,
            criado_em=escola_criada.criado_em,
            atualizado_em=escola_criada.atualizado_em,
        )
