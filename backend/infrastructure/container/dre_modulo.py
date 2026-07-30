"""
Composição das dependências relacionadas à entidade DRE.
"""

from application.use_cases.dre import (
    AtualizarDreUseCase,
    BuscarDrePorIdUseCase,
    CriarDreUseCase,
    ListarDresUseCase,
    RemoverDreUseCase,
)

from infrastructure.database.sqlite.repositories import SqliteDreRepository

from .base_modulo import BaseModulo


class DreModulo(BaseModulo):
    """
    Monta os repositórios e casos de uso relacionados à entidade DRE.

    As dependências são criadas sob demanda utilizando a conexão
    compartilhada fornecida pelo Container.
    """

    def dre_repo(self) -> SqliteDreRepository:
        """
        Retorna uma instância configurada do repositório SQLite de DRE.
        """
        return SqliteDreRepository(self._conexao)

    def criar_dre(self) -> CriarDreUseCase:
        """
        Monta o caso de uso responsável por criar uma DRE.
        """
        return CriarDreUseCase(self.dre_repo())

    def buscar_dre_por_id(self) -> BuscarDrePorIdUseCase:
        """
        Monta o caso de uso responsável por buscar uma DRE pelo
        identificador.
        """
        return BuscarDrePorIdUseCase(self.dre_repo())

    def listar_dres(self) -> ListarDresUseCase:
        """
        Monta o caso de uso responsável por listar todas as DREs.
        """
        return ListarDresUseCase(self.dre_repo())

    def atualizar_dre(self) -> AtualizarDreUseCase:
        """
        Monta o caso de uso responsável por atualizar uma DRE.
        """
        return AtualizarDreUseCase(self.dre_repo())

    def remover_dre(self) -> RemoverDreUseCase:
        """
        Monta o caso de uso responsável por remover uma DRE.
        """
        return RemoverDreUseCase(self.dre_repo())
