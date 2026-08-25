"""
Composição das dependências relacionadas à entidade Responsável.
"""

from backend.application.use_cases.responsavel import (
    AtualizarResponsavelUseCase,
    BuscarResponsavelPorCemepUseCase,
    BuscarResponsavelPorIdUseCase,
    CriarResponsavelUseCase,
    ListarResponsavelUseCase,
    RemoverResponsavelUseCase,
)

from backend.infrastructure.database.sqlite.repositories import SqliteResponsavelRepository

from .base_modulo import BaseModulo


class ResponsavelModulo(BaseModulo):
    """
    Monta os repositórios e casos de uso relacionados à entidade
    Responsável.

    As dependências são criadas sob demanda utilizando a conexão
    compartilhada fornecida pelo Container.
    """

    def responsavel_repo(self) -> SqliteResponsavelRepository:
        """
        Retorna uma instância configurada do repositório SQLite de
        Responsável.
        """
        return SqliteResponsavelRepository(self._conexao)

    def criar_responsavel(self) -> CriarResponsavelUseCase:
        """
        Monta o caso de uso responsável por criar um Responsável.
        """
        return CriarResponsavelUseCase(self.responsavel_repo())

    def buscar_responsavel_por_id(self) -> BuscarResponsavelPorIdUseCase:
        """
        Monta o caso de uso responsável por buscar um Responsável pelo
        identificador.
        """
        return BuscarResponsavelPorIdUseCase(self.responsavel_repo())

    def buscar_responsavel_por_cemep(self) -> BuscarResponsavelPorCemepUseCase:
        """
        Monta o caso de uso responsável por buscar os Responsáveis
        vinculados a um CEMEP.
        """
        return BuscarResponsavelPorCemepUseCase(self.responsavel_repo())

    def listar_responsaveis(self) -> ListarResponsavelUseCase:
        """
        Monta o caso de uso responsável por listar todos os
        Responsáveis.
        """
        return ListarResponsavelUseCase(self.responsavel_repo())

    def atualizar_responsavel(self) -> AtualizarResponsavelUseCase:
        """
        Monta o caso de uso responsável por atualizar um Responsável.
        """
        return AtualizarResponsavelUseCase(self.responsavel_repo())

    def remover_responsavel(self) -> RemoverResponsavelUseCase:
        """
        Monta o caso de uso responsável por remover um Responsável.
        """
        return RemoverResponsavelUseCase(self.responsavel_repo())
