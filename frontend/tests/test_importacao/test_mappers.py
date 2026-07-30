"""
Testes unitários de cada Mapper: linha crua -> DTO, incluindo
resolução de FK (escola_id/escola_inep, cemep_id/escola_inep) e os
casos de erro que cada um pode levantar.
"""

from __future__ import annotations

import pytest

from domain.entities import Dre
from domain.value_objects import Nome
from importacao.mappers import (
    CemepMapper,
    ChromebookMapper,
    DiretorMapper,
    DreMapper,
    EscolaMapper,
    ResponsavelMapper,
    StarlinkMapper,
    TurmaCemepMapper,
)


# ---------------------------------------------------------------------
# DreMapper — sem FK nenhuma
# ---------------------------------------------------------------------

def test_dre_mapper_com_telefone():
    entrada = DreMapper().mapear({"nome": "dre belém", "telefone": "91999998888"})

    assert entrada.nome == "dre belém"
    assert entrada.telefone == "91999998888"


def test_dre_mapper_sem_telefone_vira_none():
    entrada = DreMapper().mapear({"nome": "dre belém", "telefone": ""})

    assert entrada.telefone is None


def test_dre_mapper_sem_coluna_nome_levanta_keyerror():
    with pytest.raises(KeyError):
        DreMapper().mapear({"telefone": "91999998888"})


# ---------------------------------------------------------------------
# EscolaMapper — resolve dre_id direto ou por dre_nome
# ---------------------------------------------------------------------

def test_escola_mapper_com_dre_id_direto(repo_dre):
    entrada = EscolaMapper(repo_dre).mapear(
        {
            "inep": "12345678",
            "nome": "Escola A",
            "tipo": "municipal",
            "municipio": "Belém",
            "dre_id": "42",
        }
    )

    assert entrada.dre_id == 42
    assert entrada.tipo == "MUNICIPAL"  # normalizado em maiúsculas
    assert entrada.endereco is None


def test_escola_mapper_resolve_por_dre_nome(repo_dre, dre_salva):
    entrada = EscolaMapper(repo_dre).mapear(
        {
            "inep": "12345678",
            "nome": "Escola A",
            "tipo": "ESTADUAL",
            "municipio": "Belém",
            "dre_nome": "DRE BELÉM",  # busca é case/acento-insensível via VO Nome
        }
    )

    assert entrada.dre_id == dre_salva.id


def test_escola_mapper_sem_dre_id_nem_dre_nome_levanta_valueerror(repo_dre):
    with pytest.raises(ValueError, match="dre_id.*dre_nome"):
        EscolaMapper(repo_dre).mapear(
            {"inep": "1", "nome": "A", "tipo": "MUNICIPAL", "municipio": "Belém"}
        )


def test_escola_mapper_dre_nome_inexistente_levanta_valueerror(repo_dre):
    with pytest.raises(ValueError, match="não encontrada"):
        EscolaMapper(repo_dre).mapear(
            {
                "inep": "1",
                "nome": "A",
                "tipo": "MUNICIPAL",
                "municipio": "Belém",
                "dre_nome": "DRE que não existe",
            }
        )


def test_escola_mapper_dre_nome_ambiguo_levanta_valueerror(repo_dre):
    repo_dre.salvar(Dre(id=None, nome=Nome("DRE Duplicada"), telefone=None))
    repo_dre.salvar(Dre(id=None, nome=Nome("DRE Duplicada"), telefone=None))

    with pytest.raises(ValueError, match="Mais de uma DRE"):
        EscolaMapper(repo_dre).mapear(
            {
                "inep": "1",
                "nome": "A",
                "tipo": "MUNICIPAL",
                "municipio": "Belém",
                "dre_nome": "DRE Duplicada",
            }
        )


def test_escola_mapper_com_endereco(repo_dre):
    entrada = EscolaMapper(repo_dre).mapear(
        {
            "inep": "1",
            "nome": "A",
            "tipo": "MUNICIPAL",
            "municipio": "Belém",
            "dre_id": "1",
            "endereco": "  Rua Teste, 123  ",
        }
    )

    assert entrada.endereco == "Rua Teste, 123"


# ---------------------------------------------------------------------
# DiretorMapper — resolve escola_id direto ou por escola_inep
# ---------------------------------------------------------------------

def test_diretor_mapper_com_escola_id_direto(repo_escola):
    entrada = DiretorMapper(repo_escola).mapear(
        {"nome": "Fulano", "escola_id": "7"}
    )

    assert entrada.escola_id == 7
    assert entrada.telefone is None
    assert entrada.email is None


def test_diretor_mapper_resolve_por_escola_inep(repo_escola, escola_salva):
    entrada = DiretorMapper(repo_escola).mapear(
        {
            "nome": "Fulano",
            "escola_inep": "12345678",
            "telefone": "91988887777",
            "email": " Fulano@Escola.com ",
        }
    )

    assert entrada.escola_id == escola_salva.id
    assert entrada.email == "Fulano@Escola.com"


def test_diretor_mapper_escola_inep_inexistente_levanta_valueerror(repo_escola):
    with pytest.raises(ValueError, match="não encontrada"):
        DiretorMapper(repo_escola).mapear({"nome": "Fulano", "escola_inep": "00000000"})


def test_diretor_mapper_sem_escola_id_nem_inep_levanta_valueerror(repo_escola):
    with pytest.raises(ValueError, match="escola_id.*escola_inep"):
        DiretorMapper(repo_escola).mapear({"nome": "Fulano"})


# ---------------------------------------------------------------------
# CemepMapper — resolve escola_id direto ou por escola_inep
# ---------------------------------------------------------------------

def test_cemep_mapper_com_escola_id_direto(repo_escola):
    entrada = CemepMapper(repo_escola).mapear({"escola_id": "3", "comentario": ""})

    assert entrada.escola_id == 3
    assert entrada.comentario is None


def test_cemep_mapper_resolve_por_escola_inep(repo_escola, escola_salva):
    entrada = CemepMapper(repo_escola).mapear(
        {"escola_inep": "12345678", "comentario": "turno da tarde"}
    )

    assert entrada.escola_id == escola_salva.id
    assert entrada.comentario == "turno da tarde"


# ---------------------------------------------------------------------
# ChromebookMapper — converte kit_aluno/kit_professor para int
# ---------------------------------------------------------------------

def test_chromebook_mapper_com_valores_numericos(repo_escola):
    entrada = ChromebookMapper(repo_escola).mapear(
        {"escola_id": "5", "kit_aluno": "30", "kit_professor": "2"}
    )

    assert entrada.kit_aluno == 30
    assert entrada.kit_professor == 2
    assert isinstance(entrada.kit_aluno, int)


def test_chromebook_mapper_sem_valores_vira_none(repo_escola):
    entrada = ChromebookMapper(repo_escola).mapear(
        {"escola_id": "5", "kit_aluno": "", "kit_professor": ""}
    )

    assert entrada.kit_aluno is None
    assert entrada.kit_professor is None


def test_chromebook_mapper_valor_nao_numerico_levanta_valueerror(repo_escola):
    with pytest.raises(ValueError):
        ChromebookMapper(repo_escola).mapear({"escola_id": "5", "kit_aluno": "trinta"})


# ---------------------------------------------------------------------
# StarlinkMapper — resolve escola_id direto ou por escola_inep
# ---------------------------------------------------------------------

def test_starlink_mapper_com_escola_id(repo_escola):
    entrada = StarlinkMapper(repo_escola).mapear(
        {"escola_id": "9", "designacao": "STARLINK-01"}
    )

    assert entrada.escola_id == 9
    assert entrada.designacao == "STARLINK-01"


def test_starlink_mapper_sem_designacao_levanta_keyerror(repo_escola):
    with pytest.raises(KeyError):
        StarlinkMapper(repo_escola).mapear({"escola_id": "9"})


# ---------------------------------------------------------------------
# ResponsavelMapper — resolve cemep_id direto ou via escola_inep -> Cemep
# ---------------------------------------------------------------------

def test_responsavel_mapper_com_cemep_id_direto(repo_cemep, repo_escola):
    entrada = ResponsavelMapper(repo_cemep, repo_escola).mapear(
        {"nome": "Responsável A", "cemep_id": "11"}
    )

    assert entrada.cemep_id == 11


def test_responsavel_mapper_resolve_via_escola_inep(repo_cemep, repo_escola, cemep_salvo):
    entrada = ResponsavelMapper(repo_cemep, repo_escola).mapear(
        {"nome": "Responsável A", "escola_inep": "12345678"}
    )

    assert entrada.cemep_id == cemep_salvo.id


def test_responsavel_mapper_escola_sem_cemep_levanta_valueerror(
    repo_cemep, repo_escola, escola_salva
):
    with pytest.raises(ValueError, match="não possui CEMEP"):
        ResponsavelMapper(repo_cemep, repo_escola).mapear(
            {"nome": "Responsável A", "escola_inep": "12345678"}
        )


def test_responsavel_mapper_escola_inexistente_levanta_valueerror(repo_cemep, repo_escola):
    with pytest.raises(ValueError, match="não encontrada"):
        ResponsavelMapper(repo_cemep, repo_escola).mapear(
            {"nome": "Responsável A", "escola_inep": "00000000"}
        )


# ---------------------------------------------------------------------
# TurmaCemepMapper — só aceita responsavel_id direto (ver docstring
# da classe para a justificativa de não ter busca por nome)
# ---------------------------------------------------------------------

def test_turma_cemep_mapper_com_responsavel_id():
    entrada = TurmaCemepMapper().mapear(
        {"nome_turma": "Turma A", "responsavel_id": "21"}
    )

    assert entrada.responsavel_id == 21
    assert entrada.nome_turma == "Turma A"


def test_turma_cemep_mapper_responsavel_id_nao_numerico_levanta_valueerror():
    with pytest.raises(ValueError):
        TurmaCemepMapper().mapear({"nome_turma": "Turma A", "responsavel_id": "abc"})
