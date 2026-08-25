"""
Composição das dependências relacionadas à entidade Diretor.
"""

from backend.application.use_cases.diretor import (
    AtualizarDiretorUseCase,
    BuscarDiretorPorEscolaUseCase,
    BuscarDiretorPorIdUseCase,
    CriarDiretorUseCase,
    ListarDiretoresUseCase,
    RemoverDiretorUseCase,
)

from backend.infrastructure.database.sqlite.repositories import SqliteDiretorRepository

from .base_modulo import BaseModulo


class DiretorModulo(BaseModulo):
    """
    Monta os repositórios e casos de uso relacionados à entidade
    Diretor.

    As dependências são criadas sob demanda utilizando a conexão
    compartilhada fornecida pelo Container.
    """

    def diretor_repo(self) -> SqliteDiretorRepository:
        """
        Retorna uma instância configurada do repositório SQLite de
        Diretor.
        """
        return SqliteDiretorRepository(self._conexao)

    def criar_diretor(self) -> CriarDiretorUseCase:
        """
        Monta o caso de uso responsável por criar um Diretor.
        """
        return CriarDiretorUseCase(self.diretor_repo())

    def buscar_diretor_por_id(self) -> BuscarDiretorPorIdUseCase:
        """
        Monta o caso de uso responsável por buscar um Diretor pelo
        identificador.
        """
        return BuscarDiretorPorIdUseCase(self.diretor_repo())

    def buscar_diretor_por_escola(self) -> BuscarDiretorPorEscolaUseCase:
        """
        Monta o caso de uso responsável por buscar o Diretor vinculado
        a uma Escola.
        """
        return BuscarDiretorPorEscolaUseCase(self.diretor_repo())

    def listar_diretores(self) -> ListarDiretoresUseCase:
        """
        Monta o caso de uso responsável por listar todos os Diretores.
        """
        return ListarDiretoresUseCase(self.diretor_repo())

    def atualizar_diretor(self) -> AtualizarDiretorUseCase:
        """
        Monta o caso de uso responsável por atualizar um Diretor.
        """
        return AtualizarDiretorUseCase(self.diretor_repo())

    def remover_diretor(self) -> RemoverDiretorUseCase:
        """
        Monta o caso de uso responsável por remover um Diretor.
        """
        return RemoverDiretorUseCase(self.diretor_repo())