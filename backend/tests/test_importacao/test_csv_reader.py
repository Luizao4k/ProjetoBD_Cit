"""
Testes de importacao.readers.csv_reader.CsvReader, isolado do
Pipeline e de qualquer entidade de domínio.
"""

import inspect

from backend.infrastructure.importacao.readers import CsvReader


def _escrever_csv(caminho, cabecalho, linhas):
    import csv

    with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=cabecalho)
        escritor.writeheader()
        for linha in linhas:
            escritor.writerow(linha)


def test_ler_produz_dicts_com_as_colunas_do_cabecalho(tmp_path):
    caminho = tmp_path / "dados.csv"
    _escrever_csv(caminho, ["a", "b"], [{"a": "1", "b": "x"}, {"a": "2", "b": "y"}])

    linhas = list(CsvReader(caminho).ler())

    assert linhas == [{"a": "1", "b": "x"}, {"a": "2", "b": "y"}]


def test_ler_e_um_generator_nao_le_o_arquivo_na_hora_da_chamada(tmp_path):
    """
    Prova de streaming: chamar .ler() num arquivo que não existe não
    levanta erro nenhum — só levantaria ao iterar. Isso só é possível
    porque .ler() é uma função geradora (usa yield), não uma função
    que lê tudo e devolve uma lista pronta.
    """
    caminho_inexistente = tmp_path / "nao_existe.csv"

    gerador = CsvReader(caminho_inexistente).ler()

    assert inspect.isgenerator(gerador)


def test_total_estimado_conta_linhas_de_dado_sem_cabecalho(tmp_path):
    caminho = tmp_path / "dados.csv"
    _escrever_csv(
        caminho, ["a"], [{"a": "1"}, {"a": "2"}, {"a": "3"}]
    )

    assert CsvReader(caminho).total_estimado() == 3


def test_total_estimado_arquivo_inexistente_devolve_none(tmp_path):
    assert CsvReader(tmp_path / "nao_existe.csv").total_estimado() is None


def test_validar_arquivo_inexistente(tmp_path):
    problemas = CsvReader(tmp_path / "nao_existe.csv").validar()

    assert len(problemas) == 1
    assert "não encontrado" in problemas[0]


def test_validar_coluna_obrigatoria_ausente(tmp_path):
    caminho = tmp_path / "dados.csv"
    _escrever_csv(caminho, ["nome"], [{"nome": "a"}])

    problemas = CsvReader(caminho, colunas_obrigatorias=["nome", "inep"]).validar()

    assert len(problemas) == 1
    assert "inep" in problemas[0]


def test_validar_sem_problemas_quando_colunas_presentes(tmp_path):
    caminho = tmp_path / "dados.csv"
    _escrever_csv(caminho, ["nome", "inep"], [{"nome": "a", "inep": "12345678"}])

    problemas = CsvReader(caminho, colunas_obrigatorias=["nome", "inep"]).validar()

    assert problemas == []
