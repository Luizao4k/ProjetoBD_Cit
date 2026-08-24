"""
Testes de scripts.importar_tudo — o orquestrador de um comando só.
"""

from __future__ import annotations

import csv

from infrastructure.database import criar_conexao
from scripts.importar_tudo import importar_tudo


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


def _popular_diretorio_completo(diretorio):
    """Um diretório com as 8 entidades, encadeadas corretamente
    (mesmos dados de tests/test_importacao/test_scripts_integracao.py
    ::test_cadeia_completa_dre_at_turma_via_scripts_independentes)."""
    _escrever_csv(diretorio / "dres.csv", ["nome"], [{"nome": "dre belém"}])
    _escrever_csv(
        diretorio / "escolas.csv",
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
    _escrever_csv(
        diretorio / "diretores.csv",
        ["nome", "escola_inep"],
        [{"nome": "Fulano", "escola_inep": "12345678"}],
    )
    _escrever_csv(
        diretorio / "cemeps.csv",
        ["comentario", "escola_inep"],
        [{"comentario": "", "escola_inep": "12345678"}],
    )
    _escrever_csv(
        diretorio / "chromebooks.csv",
        ["kit_aluno", "escola_inep"],
        [{"kit_aluno": "30", "escola_inep": "12345678"}],
    )
    _escrever_csv(
        diretorio / "starlinks.csv",
        ["designacao", "escola_inep"],
        [{"designacao": "STARLINK-01", "escola_inep": "12345678"}],
    )
    _escrever_csv(
        diretorio / "responsaveis.csv",
        ["nome", "escola_inep"],
        [{"nome": "Responsável A", "escola_inep": "12345678"}],
    )
    _escrever_csv(
        diretorio / "turmas_cemep.csv",
        ["nome_turma", "responsavel_id"],
        [{"nome_turma": "Turma A", "responsavel_id": "1"}],
    )


def test_importa_as_8_entidades_na_ordem_certa(tmp_path):
    banco = str(tmp_path / "teste.db")
    _popular_diretorio_completo(tmp_path)

    relatorios = importar_tudo(tmp_path, banco)

    assert [r.nome_entidade for r in relatorios] == [
        "DRE",
        "Escola",
        "Diretor",
        "CEMEP",
        "Chromebook",
        "Starlink",
        "Responsável",
        "Turma CEMEP",
    ]
    assert all(r.resultado is not None for r in relatorios)
    assert all(len(r.resultado.erros) == 0 for r in relatorios)

    assert _contar(banco, "dres") == 1
    assert _contar(banco, "escolas") == 1
    assert _contar(banco, "diretores") == 1
    assert _contar(banco, "cemeps") == 1
    assert _contar(banco, "chromebooks") == 1
    assert _contar(banco, "starlinks") == 1
    assert _contar(banco, "responsaveis") == 1
    assert _contar(banco, "turmas_cemep") == 1


def test_entidade_sem_arquivo_e_pulada_sem_quebrar_as_outras(tmp_path):
    banco = str(tmp_path / "teste.db")
    # só dres.csv e escolas.csv -- as outras 6 não têm arquivo
    _escrever_csv(tmp_path / "dres.csv", ["nome"], [{"nome": "dre belém"}])
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

    relatorios = importar_tudo(tmp_path, banco)

    por_nome = {r.nome_entidade: r for r in relatorios}
    assert por_nome["DRE"].resultado is not None
    assert por_nome["Escola"].resultado is not None
    assert por_nome["Diretor"].resultado is None
    assert por_nome["Diretor"].arquivo is None
    assert por_nome["Diretor"].erro_arquivo is None  # pulado, não é um erro

    assert _contar(banco, "dres") == 1
    assert _contar(banco, "escolas") == 1


def test_aceita_mistura_de_csv_e_excel(tmp_path):
    from openpyxl import Workbook

    banco = str(tmp_path / "teste.db")

    # DRE via Excel, Escola via CSV -- a ordem/encadeamento não muda
    workbook = Workbook()
    workbook.active.append(["nome"])
    workbook.active.append(["dre belém"])
    workbook.save(tmp_path / "dres.xlsx")

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

    relatorios = importar_tudo(tmp_path, banco)

    por_nome = {r.nome_entidade: r for r in relatorios}
    assert por_nome["DRE"].arquivo.suffix == ".xlsx"
    assert por_nome["Escola"].arquivo.suffix == ".csv"
    assert len(por_nome["Escola"].resultado.sucessos) == 1
    assert _contar(banco, "escolas") == 1


def test_relatorio_final_soma_sucessos_e_falhas(tmp_path, capsys):
    banco = str(tmp_path / "teste.db")
    _escrever_csv(
        tmp_path / "dres.csv",
        ["nome"],
        [{"nome": "dre a"}, {"nome": "   "}],  # 1 sucesso, 1 falha
    )

    importar_tudo(tmp_path, banco)

    saida = capsys.readouterr().out
    assert "TOTAL: 1 registro(s) importado(s), 1 falha(s)" in saida
