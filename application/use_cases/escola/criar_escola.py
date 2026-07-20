"""
Caso de uso: criar uma nova Escola.
"""
from __future__ import annotations

from domain.entities import Escola
from domain.enums import TipoEscola
from domain.repositories import EscolaRepository
from domain.value_objects import Endereco, Inep, Municipio, Nome

from .dtos import CriarEscolaInput, EscolaOutput


class CriarEscolaUseCase:
    """
    Cria uma nova Escola a partir dos dados informados.
    """

    def __init__(self, repositorio: EscolaRepository) -> None:
        self._repositorio = repositorio

    def executar(self, dados: CriarEscolaInput) -> EscolaOutput:
        """
        Valida os dados (via Value Objects), persiste a nova Escola
        e retorna o DTO de saída já com o identificador gerado.

        Levanta ValueError se `dados.tipo` não corresponder a um
        TipoEscola válido (ESTADUAL ou MUNICIPAL).
        """
        escola = Escola(
            id=None,
            inep=Inep(dados.inep),
            nome=Nome(dados.nome),
            tipo=TipoEscola(dados.tipo),
            municipio=Municipio(dados.municipio),
            dre_id=dados.dre_id,
            endereco=Endereco(dados.endereco) if dados.endereco else None,
        )

        escola_criada = self._repositorio.salvar(escola)

        return EscolaOutput.de_entidade(escola_criada)
