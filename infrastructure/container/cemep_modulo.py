"""
Composição das dependências relacionadas à entidade CEMEP.
"""

from application.use_cases.cemep import (
    AtualizarCemepUseCase,
    BuscarCemepPorEscolaUseCase,
    BuscarCemepPorIdUseCase,
    CriarCemepUseCase,
    ListarCemepsUseCase,
    RemoverCemepUseCase,
)

from infrastructure.database.sqlite.repositories import SqliteCemepRepository

from .base_modulo import BaseModulo


class CemepModulo(BaseModulo):
    """
    Monta os repositórios e casos de uso relacionados à entidade
    CEMEP.

    As dependências são criadas sob demanda utilizando a conexão
    compartilhada fornecida pelo Container.
    """

    def cemep_repo(self) -> SqliteCemepRepository:
        """
        Retorna uma instância configurada do repositório SQLite de
        CEMEP.
        """
        return SqliteCemepRepository(self._conexao)

    def criar_cemep(self) -> CriarCemepUseCase:
        """
        Monta o caso de uso responsável por criar um CEMEP.
        """
        return CriarCemepUseCase(self.cemep_repo())

    def buscar_cemep_por_id(self) -> BuscarCemepPorIdUseCase:
        """
        Monta o caso de uso responsável por buscar um CEMEP pelo
        identificador.
        """
        return BuscarCemepPorIdUseCase(self.cemep_repo())

    def buscar_cemep_por_escola(self) -> BuscarCemepPorEscolaUseCase:
        """
        Monta o caso de uso responsável por buscar o CEMEP vinculado
        a uma Escola.
        """
        return BuscarCemepPorEscolaUseCase(self.cemep_repo())

    def listar_cemeps(self) -> ListarCemepsUseCase:
        """
        Monta o caso de uso responsável por listar todos os CEMEPs.
        """
        return ListarCemepsUseCase(self.cemep_repo())

    def atualizar_cemep(self) -> AtualizarCemepUseCase:
        """
        Monta o caso de uso responsável por atualizar um CEMEP.
        """
        return AtualizarCemepUseCase(self.cemep_repo())

    def remover_cemep(self) -> RemoverCemepUseCase:
        """
        Monta o caso de uso responsável por remover um CEMEP.
        """
        return RemoverCemepUseCase(self.cemep_repo())
