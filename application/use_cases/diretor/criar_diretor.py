"""
Caso de uso: criar um novo Diretor.
"""
from __future__ import annotations

from domain.entities import Diretor
from domain.repositories import DiretorRepository
from domain.value_objects import Email, Nome, Telefone

from .dtos import CriarDiretorInput, DiretorOutput


class CriarDiretorUseCase:
    """
    Cria um novo Diretor vinculado a uma Escola.

    Não valida aqui se a escola já possui outro diretor (relação
    1:1) — essa checagem de unicidade é responsabilidade da camada
    de persistência/infraestrutura, não do caso de uso.
    """

    def __init__(self, repositorio: DiretorRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dados: CriarDiretorInput) -> DiretorOutput:
        diretor = Diretor(
            id=None,
            escola_id=dados.escola_id,
            nome=Nome(dados.nome),
            telefone=Telefone(dados.telefone) if dados.telefone else None,
            email=Email(dados.email) if dados.email else None,
        )

        diretor_criado = self._repositorio.salvar(diretor)

        return DiretorOutput.de_entidade(diretor_criado)
