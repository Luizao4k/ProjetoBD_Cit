"""
Testes de scripts.importar_escolas.
"""

import csv

import pytest

from infrastructure.database import criar_conexao, criar_schema
from infrastructure.database.sqlite.repositories import SqliteDreRepository
from domain.entities import Dre
from domain.value_objects import Nome
from scripts.importar_escolas import (
    resolver_dre_id,
    montar_entrada_escola,
    importar_escolas,
)


@pytest.fixture
def conexao():
    conn = criar_conexao(":memory:")
    criar_schema(conn)
    yield conn
    conn.close()


@pytest.fixture
def repo_dre(conexao):
    return SqliteDreRepository(conexao)


# ---------------------------------------------------------------------
# resolver_dre_id
# ---------------------------------------------------------------------

def test_resolver_dre_id_usa_dre_id_direto_quando_informado(repo_dre):
    resultado = resolver_dre_id({"dre_id": "42", "dre_nome": ""}, repo_dre)
    assert resultado == 42


def test_resolver_dre_id_resolve_por_nome(repo_dre):
    dre = repo_dre.salvar(Dre(id=None, nome=Nome("dre belém"), telefone=None))

    resultado = resolver_dre_id({"dre_id": "", "dre_nome": "dre belém"}, repo_dre)

    assert resultado == dre.id


def test_resolver_dre_id_falha_quando_nome_nao_encontrado(repo_dre):
    with pytest.raises(ValueError, match="não encontrada"):
        resolver_dre_id({"dre_id": "", "dre_nome": "dre fantasma"}, repo_dre)


def test_resolver_dre_id_falha_quando_nada_informado(repo_dre):
    with pytest.raises(ValueError, match="não informou"):
        resolver_dre_id({"dre_id": "", "dre_nome": ""}, repo_dre)


def test_resolver_dre_id_falha_quando_nome_e_ambiguo(repo_dre):
    from domain.entities import Dre

    repo_dre.salvar(Dre(id=None, nome=Nome("dre duplicada"), telefone=None))
    repo_dre.salvar(Dre(id=None, nome=Nome("dre duplicada"), telefone=None))

    with pytest.raises(ValueError, match="Mais de uma DRE"):
        resolver_dre_id({"dre_id": "", "dre_nome": "dre duplicada"}, repo_dre)


# ---------------------------------------------------------------------
# montar_entrada_escola
# ---------------------------------------------------------------------

def test_montar_entrada_escola_com_endereco(repo_dre):
    linha = {
        "inep": "15000001",
        "nome": "escola alfa",
        "tipo": "municipal",
        "municipio": "Belém",
        "endereco": "Rua Tal, 100",
        "dre_id": "1",
        "dre_nome": "",
    }

    entrada = montar_entrada_escola(linha, repo_dre)

    assert entrada.inep == "15000001"
    assert entrada.tipo == "MUNICIPAL"
    assert entrada.dre_id == 1
    assert entrada.endereco == "Rua Tal, 100"


def test_montar_entrada_escola_sem_endereco_vira_none(repo_dre):
    linha = {
        "inep": "15000001",
        "nome": "escola alfa",
        "tipo": "estadual",
        "municipio": "Belém",
        "endereco": "",
        "dre_id": "1",
        "dre_nome": "",
    }

    entrada = montar_entrada_escola(linha, repo_dre)

    assert entrada.endereco is None


def test_montar_entrada_escola_sem_coluna_obrigatoria_levanta_keyerror(repo_dre):
    linha = {"nome": "escola sem inep", "tipo": "estadual", "municipio": "Belém",
              "dre_id": "1", "dre_nome": ""}

    with pytest.raises(KeyError):
        montar_entrada_escola(linha, repo_dre)


# ---------------------------------------------------------------------
# importar_escolas — fim a fim, com CSV e banco reais
# ---------------------------------------------------------------------

def test_importar_escolas_fim_a_fim(tmp_path):
    caminho_banco = str(tmp_path / "teste.db")

    conexao = criar_conexao(caminho_banco)
    criar_schema(conexao)
    dre = SqliteDreRepository(conexao).salvar(
        Dre(id=None, nome=Nome("dre belém"), telefone=None)
    )
    conexao.close()

    caminho_csv = tmp_path / "escolas.csv"
    with open(caminho_csv, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=["inep", "nome", "tipo", "municipio", "endereco", "dre_id", "dre_nome"],
        )
        escritor.writeheader()
        # linha 1: válida, por dre_id
        escritor.writerow({
            "inep": "15000001", "nome": "escola valida um", "tipo": "MUNICIPAL",
            "municipio": "Belém", "endereco": "", "dre_id": str(dre.id), "dre_nome": "",
        })
        # linha 2: válida, por dre_nome
        escritor.writerow({
            "inep": "15000002", "nome": "escola valida dois", "tipo": "ESTADUAL",
            "municipio": "Marabá", "endereco": "", "dre_id": "", "dre_nome": "dre belém",
        })
        # linha 3: INEP duplicado da linha 1 -> deve falhar
        escritor.writerow({
            "inep": "15000001", "nome": "escola duplicada", "tipo": "MUNICIPAL",
            "municipio": "Belém", "endereco": "", "dre_id": str(dre.id), "dre_nome": "",
        })
        # linha 4: DRE inexistente -> deve falhar
        escritor.writerow({
            "inep": "15000004", "nome": "escola orfa", "tipo": "MUNICIPAL",
            "municipio": "Belém", "endereco": "", "dre_id": "", "dre_nome": "dre fantasma",
        })

    importar_escolas(caminho_csv, caminho_banco)

    caminho_falhas = tmp_path / "escolas_falhas.csv"
    assert caminho_falhas.exists()

    with open(caminho_falhas, encoding="utf-8", newline="") as arquivo:
        falhas = list(csv.DictReader(arquivo))

    assert len(falhas) == 2
    assert falhas[0]["numero_linha"] == "3"
    assert "InepJaCadastradoError" in falhas[0]["tipo_erro"]
    assert falhas[1]["numero_linha"] == "4"
    assert "ValueError" in falhas[1]["tipo_erro"]

    conexao_verificacao = criar_conexao(caminho_banco)
    total_escolas = conexao_verificacao.execute("SELECT COUNT(*) FROM escolas").fetchone()[0]
    conexao_verificacao.close()
    assert total_escolas == 2
