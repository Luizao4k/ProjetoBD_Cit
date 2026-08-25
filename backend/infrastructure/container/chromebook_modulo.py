"""
Composição das dependências relacionadas à entidade Chromebook.
"""

from backend.application.use_cases.chromebook import (
    AtualizarChromebookUseCase,
    BuscarChromebookPorEscolaUseCase,
    BuscarChromebookPorIdUseCase,
    CriarChromebookUseCase,
    ListarChromebooksUseCase,
    RemoverChromebookUseCase,
)

from backend.infrastructure.database.sqlite.repositories import SqliteChromebookRepository

from .base_modulo import BaseModulo


class ChromebookModulo(BaseModulo):
    """
    Monta os repositórios e casos de uso relacionados à entidade
    Chromebook.

    As dependências são criadas sob demanda utilizando a conexão
    compartilhada fornecida pelo Container.
    """

    def chromebook_repo(self) -> SqliteChromebookRepository:
        """
        Retorna uma instância configurada do repositório SQLite de
        Chromebook.
        """
        return SqliteChromebookRepository(self._conexao)

    def criar_chromebook(self) -> CriarChromebookUseCase:
        """
        Monta o caso de uso responsável por criar um Chromebook.
        """
        return CriarChromebookUseCase(self.chromebook_repo())

    def buscar_chromebook_por_id(self) -> BuscarChromebookPorIdUseCase:
        """
        Monta o caso de uso responsável por buscar um Chromebook pelo
        identificador.
        """
        return BuscarChromebookPorIdUseCase(self.chromebook_repo())

    def buscar_chromebook_por_escola(self) -> BuscarChromebookPorEscolaUseCase:
        """
        Monta o caso de uso responsável por buscar o registro de
        Chromebook vinculado a uma Escola.
        """
        return BuscarChromebookPorEscolaUseCase(self.chromebook_repo())

    def listar_chromebooks(self) -> ListarChromebooksUseCase:
        """
        Monta o caso de uso responsável por listar todos os registros
        de Chromebook.
        """
        return ListarChromebooksUseCase(self.chromebook_repo())

    def atualizar_chromebook(self) -> AtualizarChromebookUseCase:
        """
        Monta o caso de uso responsável por atualizar um Chromebook.
        """
        return AtualizarChromebookUseCase(self.chromebook_repo())

    def remover_chromebook(self) -> RemoverChromebookUseCase:
        """
        Monta o caso de uso responsável por remover um Chromebook.
        """
        return RemoverChromebookUseCase(self.chromebook_repo())
