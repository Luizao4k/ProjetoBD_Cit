"""
Composição das dependências relacionadas à entidade Escola.
"""

from application.use_cases.escola import (
    AtualizarEscolaUseCase,
    BuscarEscolaPorIdUseCase,
    BuscarEscolasPorDreUseCase,
    CriarEscolaUseCase,
    ListarEscolasUseCase,
    RemoverEscolaUseCase,
)

from infrastructure.database.sqlite.repositories import SqliteEscolaRepository
from .base_modulo import BaseModulo


class EscolaModulo(BaseModulo):
    """
    Monta os repositórios e casos de uso relacionados à entidade
    Escola.

    As dependências são criadas sob demanda utilizando a conexão
    compartilhada fornecida pelo Container.
    """

    def escola_repo(self) -> SqliteEscolaRepository:
        """
        Retorna uma instância configurada do repositório SQLite de Escola.
        """
        return SqliteEscolaRepository(self._conexao)

    def criar_escola(self) -> CriarEscolaUseCase:
        """
        Monta o caso de uso responsável por criar uma Escola.
        """
        return CriarEscolaUseCase(self.escola_repo())

    def buscar_escola_por_id(self) -> BuscarEscolaPorIdUseCase:
        """
        Monta o caso de uso responsável por buscar uma Escola pelo
        identificador.
        """
        return BuscarEscolaPorIdUseCase(self.escola_repo())

    def buscar_escolas_por_dre(self) -> BuscarEscolasPorDreUseCase:
        """
        Monta o caso de uso responsável por listar as Escolas de uma DRE.
        """
        return BuscarEscolasPorDreUseCase(self.escola_repo())

    def listar_escolas(self) -> ListarEscolasUseCase:
        """
        Monta o caso de uso responsável por listar todas as Escolas.
        """
        return ListarEscolasUseCase(self.escola_repo())

    def atualizar_escola(self) -> AtualizarEscolaUseCase:
        """
        Monta o caso de uso responsável por atualizar uma Escola.
        """
        return AtualizarEscolaUseCase(self.escola_repo())

    def remover_escola(self) -> RemoverEscolaUseCase:
        """
        Monta o caso de uso responsável por remover uma Escola.
        """
        return RemoverEscolaUseCase(self.escola_repo())
