"""
Testes do utilitário genérico de importação em lote.
"""

import csv

import pytest

from scripts._importador_util import (
    importar_em_lote,
    ler_csv,
    exportar_falhas_csv,
)


def test_todas_as_linhas_com_sucesso():
    linhas = [{"valor": "1"}, {"valor": "2"}, {"valor": "3"}]

    resultado = importar_em_lote(
        linhas,
        montar_entrada=lambda linha: int(linha["valor"]),
        executar=lambda n: n * 10,
    )

    assert resultado.sucesso == [10, 20, 30]
    assert resultado.falhas == []
    assert resultado.total == 3


def test_linha_ruim_nao_interrompe_as_demais():
    linhas = [{"valor": "1"}, {"valor": "abc"}, {"valor": "3"}]

    resultado = importar_em_lote(
        linhas,
        montar_entrada=lambda linha: int(linha["valor"]),  # "abc" levanta ValueError
        executar=lambda n: n * 10,
    )

    assert resultado.sucesso == [10, 30]
    assert len(resultado.falhas) == 1
    assert resultado.total == 3


def test_falha_registra_numero_linha_dados_e_motivo():
    linhas = [{"valor": "1"}, {"valor": "abc"}]

    resultado = importar_em_lote(
        linhas,
        montar_entrada=lambda linha: int(linha["valor"]),
        executar=lambda n: n,
    )

    falha = resultado.falhas[0]
    assert falha.numero_linha == 2
    assert falha.dados_originais == {"valor": "abc"}
    assert falha.tipo_erro == "ValueError"
    assert "abc" in falha.motivo


def test_falha_tambem_pode_vir_da_execucao_do_caso_de_uso():
    def executar(n):
        if n == 2:
            raise RuntimeError("falha simulada do caso de uso")
        return n

    resultado = importar_em_lote(
        [{"valor": "1"}, {"valor": "2"}, {"valor": "3"}],
        montar_entrada=lambda linha: int(linha["valor"]),
        executar=executar,
    )

    assert resultado.sucesso == [1, 3]
    assert len(resultado.falhas) == 1
    assert resultado.falhas[0].tipo_erro == "RuntimeError"


def test_resumo_formata_contagem():
    resultado = importar_em_lote(
        [{"valor": "1"}, {"valor": "x"}],
        montar_entrada=lambda linha: int(linha["valor"]),
        executar=lambda n: n,
    )

    assert resultado.resumo() == "1/2 linha(s) importada(s) com sucesso, 1 falha(s)."


def test_ler_csv(tmp_path):
    caminho = tmp_path / "entrada.csv"
    caminho.write_text("nome,idade\nAna,30\nBeto,25\n", encoding="utf-8")

    linhas = ler_csv(caminho)

    assert linhas == [
        {"nome": "Ana", "idade": "30"},
        {"nome": "Beto", "idade": "25"},
    ]


def test_exportar_falhas_csv_grava_colunas_originais_mais_motivo(tmp_path):
    linhas = [{"nome": "Ana", "idade": "trinta"}]
    resultado = importar_em_lote(
        linhas,
        montar_entrada=lambda linha: int(linha["idade"]),
        executar=lambda n: n,
    )

    caminho_saida = tmp_path / "falhas.csv"
    exportar_falhas_csv(resultado, caminho_saida)

    with open(caminho_saida, encoding="utf-8", newline="") as arquivo:
        linhas_lidas = list(csv.DictReader(arquivo))

    assert len(linhas_lidas) == 1
    assert linhas_lidas[0]["nome"] == "Ana"
    assert linhas_lidas[0]["idade"] == "trinta"
    assert linhas_lidas[0]["numero_linha"] == "1"
    assert linhas_lidas[0]["tipo_erro"] == "ValueError"


def test_exportar_falhas_csv_nao_cria_arquivo_se_nao_houver_falhas(tmp_path):
    resultado = importar_em_lote(
        [{"valor": "1"}],
        montar_entrada=lambda linha: int(linha["valor"]),
        executar=lambda n: n,
    )

    caminho_saida = tmp_path / "falhas.csv"
    exportar_falhas_csv(resultado, caminho_saida)

    assert not caminho_saida.exists()
