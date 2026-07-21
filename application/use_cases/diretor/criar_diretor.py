"""
Caso de uso: criar um novo Diretor.
"""

from __future__ import annotations

from domain.entities import Diretor
from domain.repositories import DiretorRepository
from domain.value_objects import Email, Nome, Telefone
from shared.exceptions import PersistenciaInconsistenteError
from shared.types import EscolaId

from .dtos import CriarDiretorInput, DiretorOutput


class CriarDiretorUseCase:
    """
    Cria um novo Diretor vinculado a uma escola.

    A verificação de unicidade (uma escola possuir apenas um
    diretor) é responsabilidade da camada de persistência.
    """

    def __init__(self, repositorio: DiretorRepository) -> None:
        """
        Inicializa o caso de uso.

        Args:
            repositorio:
                Repositório responsável pela persistência dos Diretores.
        """
        self._repositorio = repositorio

    def executar(self, dados: CriarDiretorInput) -> DiretorOutput:
        """
        Cria um novo Diretor.

        Args:
            dados:
                Dados necessários para a criação do Diretor.

        Returns:
            DTO contendo os dados do Diretor criado.

        Raises:
            PersistenciaInconsistenteError:
                Caso o repositório retorne uma entidade persistida
                em estado inconsistente.
        """

        diretor = Diretor(
            id=None,
            escola_id=EscolaId(dados.escola_id),
            nome=Nome(dados.nome),
            telefone=Telefone(dados.telefone) if dados.telefone else None,
            email=Email(dados.email) if dados.email else None,
        )

        diretor_criado = self._repositorio.salvar(diretor)

        if diretor_criado.id is None:
            raise PersistenciaInconsistenteError(
                "O repositório retornou um Diretor sem id."
            )

        return DiretorOutput(
            id=diretor_criado.id,
            escola_id=diretor_criado.escola_id,
            nome=diretor_criado.nome.valor,
            telefone=diretor_criado.telefone.valor if diretor_criado.telefone else None,
            email=diretor_criado.email.valor if diretor_criado.email else None,
            criado_em=diretor_criado.criado_em,
            atualizado_em=diretor_criado.atualizado_em,
        )
