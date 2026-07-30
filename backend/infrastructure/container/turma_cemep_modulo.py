"""
Composição das dependências relacionadas à entidade Turma CEMEP.
"""

from application.use_cases.turma_cemep import (
    AtualizarTurmaCemepUseCase,
    BuscarTurmaCemepPorIdUseCase,
    BuscarTurmasPorResponsavelUseCase,
    CriarTurmaCemepUseCase,
    ListarTurmasCemepUseCase,
    RemoverTurmaCemepUseCase,
)

from infrastructure.database.sqlite.repositories import SqliteTurmaCemepRepository

from .base_modulo import BaseModulo


class TurmaCemepModulo(BaseModulo):
    """
    Monta os repositórios e casos de uso relacionados à entidade
    Turma CEMEP.

    As dependências são criadas sob demanda utilizando a conexão
    compartilhada fornecida pelo Container.
    """

    def turma_cemep_repo(self) -> SqliteTurmaCemepRepository:
        """
        Retorna uma instância configurada do repositório SQLite de
        Turma CEMEP.
        """
        return SqliteTurmaCemepRepository(self._conexao)

    def criar_turma_cemep(self) -> CriarTurmaCemepUseCase:
        """
        Monta o caso de uso responsável por criar uma Turma CEMEP.
        """
        return CriarTurmaCemepUseCase(self.turma_cemep_repo())

    def buscar_turma_cemep_por_id(self) -> BuscarTurmaCemepPorIdUseCase:
        """
        Monta o caso de uso responsável por buscar uma Turma CEMEP
        pelo identificador.
        """
        return BuscarTurmaCemepPorIdUseCase(self.turma_cemep_repo())

    def buscar_turmas_por_responsavel(self) -> BuscarTurmasPorResponsavelUseCase:
        """
        Monta o caso de uso responsável por buscar as Turmas CEMEP
        vinculadas a um Responsável.
        """
        return BuscarTurmasPorResponsavelUseCase(self.turma_cemep_repo())

    def listar_turmas_cemep(self) -> ListarTurmasCemepUseCase:
        """
        Monta o caso de uso responsável por listar todas as Turmas
        CEMEP.
        """
        return ListarTurmasCemepUseCase(self.turma_cemep_repo())

    def atualizar_turma_cemep(self) -> AtualizarTurmaCemepUseCase:
        """
        Monta o caso de uso responsável por atualizar uma Turma
        CEMEP.
        """
        return AtualizarTurmaCemepUseCase(self.turma_cemep_repo())

    def remover_turma_cemep(self) -> RemoverTurmaCemepUseCase:
        """
        Monta o caso de uso responsável por remover uma Turma CEMEP.
        """
        return RemoverTurmaCemepUseCase(self.turma_cemep_repo())
