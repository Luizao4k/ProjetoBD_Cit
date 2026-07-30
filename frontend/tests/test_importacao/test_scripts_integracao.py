"""
Testes de integração fim-a-fim: CSV real -> script -> banco real
(arquivo em tmp_path, não em memória, porque cada teste roda o script
via sua função pública, exatamente como um usuário rodaria via CLI).
"""

from __future__ import annotations

import csv

from infrastructure.database import criar_conexao

from scripts.importar_dres import importar_dres
from scripts.importar_escolas import importar_escolas
from scripts.importar_diretores import importar_diretores
from scripts.importar_cemeps import importar_cemeps
from scripts.importar_chromebooks import importar_chromebooks
from scripts.importar_starlinks import importar_starlinks
from scripts.importar_responsaveis import importar_responsaveis
from scripts.importar_turmas_cemep import importar_turmas_cemep


def _escrever_csv(caminho, cabecalho, linhas):
    with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=cabecalho)
        escritor.writeheader()
        for linha in linhas:
            escritor.writerow(linha)


def _contar(caminho_banco, tabela):
    conexao = criar_conexao(caminho_banco)
    total = conexao.execute(f"SELECT COUNT(*) FROM {tabela}").fetchone()[0]
    conexao.close()
    return total


# ---------------------------------------------------------------------

def test_importar_dres_fim_a_fim(tmp_path):
    banco = str(tmp_path / "teste.db")
    csv_path = tmp_path / "dres.csv"
    _escrever_csv(
        csv_path,
        ["nome", "telefone"],
        [
            {"nome": "dre belém", "telefone": "91999998888"},
            {"nome": "dre marabá", "telefone": ""},
            {"nome": "   ", "telefone": ""},  # nome vazio -> falha
        ],
    )

    resultado = importar_dres(csv_path, banco)

    assert len(resultado.sucessos) == 2
    assert len(resultado.erros) == 1
    assert resultado.erros[0].tipo_erro == "NomeInvalidoError"
    assert (tmp_path / "dres_falhas.csv").exists()
    assert _contar(banco, "dres") == 2


def test_importar_escolas_fim_a_fim(tmp_path):
    banco = str(tmp_path / "teste.db")

    _escrever_csv(tmp_path / "dres.csv", ["nome"], [{"nome": "dre belém"}])
    importar_dres(tmp_path / "dres.csv", banco)

    _escrever_csv(
        tmp_path / "escolas.csv",
        ["inep", "nome", "tipo", "municipio", "dre_nome"],
        [
            {
                "inep": "12345678",
                "nome": "Escola A",
                "tipo": "municipal",
                "municipio": "Belém",
                "dre_nome": "dre belém",
            },
            {
                # dre_nome não existe -> falha
                "inep": "87654321",
                "nome": "Escola B",
                "tipo": "ESTADUAL",
                "municipio": "Belém",
                "dre_nome": "dre que não existe",
            },
        ],
    )

    resultado = importar_escolas(tmp_path / "escolas.csv", banco)

    assert len(resultado.sucessos) == 1
    assert len(resultado.erros) == 1
    assert _contar(banco, "escolas") == 1


def _preparar_escola(tmp_path, banco):
    """Deixa uma DRE e uma Escola já cadastradas — usado pelos testes
    de Diretor/CEMEP/Chromebook/Starlink, que só precisam de uma
    Escola existente."""
    _escrever_csv(tmp_path / "dres.csv", ["nome"], [{"nome": "dre belém"}])
    importar_dres(tmp_path / "dres.csv", banco)

    _escrever_csv(
        tmp_path / "escolas.csv",
        ["inep", "nome", "tipo", "municipio", "dre_nome"],
        [
            {
                "inep": "12345678",
                "nome": "Escola A",
                "tipo": "MUNICIPAL",
                "municipio": "Belém",
                "dre_nome": "dre belém",
            }
        ],
    )
    importar_escolas(tmp_path / "escolas.csv", banco)


def test_importar_diretores_fim_a_fim(tmp_path):
    banco = str(tmp_path / "teste.db")
    _preparar_escola(tmp_path, banco)

    _escrever_csv(
        tmp_path / "diretores.csv",
        ["nome", "telefone", "email", "escola_inep"],
        [
            {"nome": "Fulano", "telefone": "91988887777", "email": "fulano@escola.com", "escola_inep": "12345678"},
            {"nome": "Ciclano", "telefone": "", "email": "", "escola_inep": "12345678"},  # 2ª p/ mesma escola -> falha
        ],
    )

    resultado = importar_diretores(tmp_path / "diretores.csv", banco)

    assert len(resultado.sucessos) == 1
    assert len(resultado.erros) == 1
    assert resultado.erros[0].tipo_erro == "EscolaJaPossuiDiretorError"
    assert _contar(banco, "diretores") == 1


def test_importar_cemeps_fim_a_fim(tmp_path):
    banco = str(tmp_path / "teste.db")
    _preparar_escola(tmp_path, banco)

    _escrever_csv(
        tmp_path / "cemeps.csv",
        ["comentario", "escola_inep"],
        [
            {"comentario": "turno da tarde", "escola_inep": "12345678"},
            {"comentario": "", "escola_inep": "00000000"},  # escola não existe -> falha
        ],
    )

    resultado = importar_cemeps(tmp_path / "cemeps.csv", banco)

    assert len(resultado.sucessos) == 1
    assert len(resultado.erros) == 1
    assert _contar(banco, "cemeps") == 1


def test_importar_chromebooks_fim_a_fim(tmp_path):
    banco = str(tmp_path / "teste.db")
    _preparar_escola(tmp_path, banco)

    _escrever_csv(
        tmp_path / "chromebooks.csv",
        ["kit_aluno", "kit_professor", "escola_inep"],
        [
            {"kit_aluno": "30", "kit_professor": "2", "escola_inep": "12345678"},
        ],
    )

    resultado = importar_chromebooks(tmp_path / "chromebooks.csv", banco)

    assert len(resultado.sucessos) == 1
    assert len(resultado.erros) == 0
    assert _contar(banco, "chromebooks") == 1


def test_importar_starlinks_fim_a_fim(tmp_path):
    banco = str(tmp_path / "teste.db")
    _preparar_escola(tmp_path, banco)

    _escrever_csv(
        tmp_path / "starlinks.csv",
        ["designacao", "escola_inep"],
        [
            {"designacao": "STARLINK-01", "escola_inep": "12345678"},
            {"designacao": "STARLINK-02", "escola_inep": "12345678"},  # mesma escola, permitido
        ],
    )

    resultado = importar_starlinks(tmp_path / "starlinks.csv", banco)

    assert len(resultado.sucessos) == 2
    assert len(resultado.erros) == 0
    assert _contar(banco, "starlinks") == 2


def _preparar_cemep(tmp_path, banco):
    """Além da Escola, deixa um CEMEP já cadastrado — usado pelos
    testes de Responsável."""
    _preparar_escola(tmp_path, banco)
    _escrever_csv(
        tmp_path / "cemeps.csv", ["comentario", "escola_inep"], [{"comentario": "", "escola_inep": "12345678"}]
    )
    importar_cemeps(tmp_path / "cemeps.csv", banco)


def test_importar_responsaveis_fim_a_fim(tmp_path):
    banco = str(tmp_path / "teste.db")
    _preparar_cemep(tmp_path, banco)

    _escrever_csv(
        tmp_path / "responsaveis.csv",
        ["nome", "escola_inep"],
        [
            {"nome": "Responsável A", "escola_inep": "12345678"},
            {"nome": "Responsável B", "escola_inep": "00000000"},  # escola não existe -> falha
        ],
    )

    resultado = importar_responsaveis(tmp_path / "responsaveis.csv", banco)

    assert len(resultado.sucessos) == 1
    assert len(resultado.erros) == 1
    assert _contar(banco, "responsaveis") == 1


def test_importar_turmas_cemep_fim_a_fim(tmp_path):
    banco = str(tmp_path / "teste.db")
    _preparar_cemep(tmp_path, banco)

    _escrever_csv(
        tmp_path / "responsaveis.csv", ["nome", "escola_inep"], [{"nome": "Responsável A", "escola_inep": "12345678"}]
    )
    importar_responsaveis(tmp_path / "responsaveis.csv", banco)

    conexao = criar_conexao(banco)
    responsavel_id = conexao.execute("SELECT id FROM responsaveis").fetchone()[0]
    conexao.close()

    _escrever_csv(
        tmp_path / "turmas.csv",
        ["nome_turma", "responsavel_id"],
        [
            {"nome_turma": "Turma A", "responsavel_id": str(responsavel_id)},
            {"nome_turma": "Turma B", "responsavel_id": "9999"},  # responsável não existe -> falha
        ],
    )

    resultado = importar_turmas_cemep(tmp_path / "turmas.csv", banco)

    assert len(resultado.sucessos) == 1
    assert len(resultado.erros) == 1
    assert resultado.erros[0].tipo_erro == "ResponsavelNaoEncontradoError"
    assert _contar(banco, "turmas_cemep") == 1


# ---------------------------------------------------------------------

def test_cadeia_completa_dre_at_turma_via_scripts_independentes(tmp_path):
    """
    Prova de que a ordem de dependência real (DRE -> Escola -> CEMEP
    -> Responsável -> Turma) funciona rodando cada script de forma
    isolada, um após o outro, sobre o MESMO banco — exatamente como
    seria feito manualmente na Fase 4 de importação inicial.
    """
    banco = str(tmp_path / "cadeia.db")

    _escrever_csv(tmp_path / "dres.csv", ["nome"], [{"nome": "dre belém"}])
    importar_dres(tmp_path / "dres.csv", banco)

    _escrever_csv(
        tmp_path / "escolas.csv",
        ["inep", "nome", "tipo", "municipio", "dre_nome"],
        [{"inep": "12345678", "nome": "Escola A", "tipo": "MUNICIPAL", "municipio": "Belém", "dre_nome": "dre belém"}],
    )
    importar_escolas(tmp_path / "escolas.csv", banco)

    _escrever_csv(
        tmp_path / "cemeps.csv", ["comentario", "escola_inep"], [{"comentario": "", "escola_inep": "12345678"}]
    )
    importar_cemeps(tmp_path / "cemeps.csv", banco)

    _escrever_csv(
        tmp_path / "responsaveis.csv", ["nome", "escola_inep"], [{"nome": "Responsável A", "escola_inep": "12345678"}]
    )
    importar_responsaveis(tmp_path / "responsaveis.csv", banco)

    conexao = criar_conexao(banco)
    responsavel_id = conexao.execute("SELECT id FROM responsaveis").fetchone()[0]
    conexao.close()

    _escrever_csv(
        tmp_path / "turmas.csv",
        ["nome_turma", "responsavel_id"],
        [{"nome_turma": "Turma A", "responsavel_id": str(responsavel_id)}],
    )
    resultado_turma = importar_turmas_cemep(tmp_path / "turmas.csv", banco)

    assert len(resultado_turma.sucessos) == 1
    assert _contar(banco, "dres") == 1
    assert _contar(banco, "escolas") == 1
    assert _contar(banco, "cemeps") == 1
    assert _contar(banco, "responsaveis") == 1
    assert _contar(banco, "turmas_cemep") == 1
