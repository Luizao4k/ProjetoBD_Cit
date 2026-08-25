"""
Composição das dependências relacionadas à entidade Starlink.
"""

from application.use_cases.starlink import (
    CriarStarlinkUseCase,
    BuscarStarlinkPorIdUseCase,
    BuscarStarlinksPorEscolaUseCase,
    ListarStarlinksUseCase,
    AtualizarStarlinkUseCase,
    RemoverStarlinkUseCase,
)

from infrastructure.database.sqlite.repositories import SqliteStarlinkRepository

from .base_modulo import BaseModulo


class StarlinkModulo(BaseModulo):
    """
    Monta os repositórios e casos de uso relacionados à entidade
    Starlink.

    As dependências são criadas sob demanda utilizando a conexão
    compartilhada fornecida pelo Container.
    """

    def starlink_repo(self) -> SqliteStarlinkRepository:
        """
        Retorna uma instância configurada do repositório SQLite de
        Starlink.
        """
        return SqliteStarlinkRepository(self._conexao)

    def criar_starlink(self) -> CriarStarlinkUseCase:
        """
        Monta o caso de uso responsável por criar um registro de
        Starlink.
        """
        return CriarStarlinkUseCase(self.starlink_repo())

    def buscar_starlink_por_id(self) -> BuscarStarlinkPorIdUseCase:
        """
        Monta o caso de uso responsável por buscar um registro de
        Starlink pelo identificador.
        """
        return BuscarStarlinkPorIdUseCase(self.starlink_repo())

    def buscar_starlink_por_escola(self) -> BuscarStarlinksPorEscolaUseCase:
        """
        Monta o caso de uso responsável por buscar o registro de
        Starlink vinculado a uma Escola.
        """
        return BuscarStarlinksPorEscolaUseCase(self.starlink_repo())

    def listar_starlinks(self) -> ListarStarlinksUseCase:
        """
        Monta o caso de uso responsável por listar todos os registros
        de Starlink.
        """
        return ListarStarlinksUseCase(self.starlink_repo())

    def atualizar_starlink(self) -> AtualizarStarlinkUseCase:
        """
        Monta o caso de uso responsável por atualizar um registro de
        Starlink.
        """
        return AtualizarStarlinkUseCase(self.starlink_repo())

    def remover_starlink(self) -> RemoverStarlinkUseCase:
        """
        Monta o caso de uso responsável por remover um registro de
        Starlink.
        """
        return RemoverStarlinkUseCase(self.starlink_repo())
