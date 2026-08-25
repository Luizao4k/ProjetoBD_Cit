"""
Testes de importacao.readers.excel_reader.ExcelReader — mesma
cobertura de test_csv_reader.py, provando que os dois Readers se
comportam de forma equivalente pro resto do pipeline.
"""

from __future__ import annotations

from openpyxl import Workbook

from infrastructure.importacao.readers import ExcelReader


def _escrever_xlsx(caminho, cabecalho, linhas, aba=None):
    workbook = Workbook()
    planilha = workbook.active
    if aba:
        planilha.title = aba
    planilha.append(cabecalho)
    for linha in linhas:
        planilha.append([linha.get(coluna) for coluna in cabecalho])
    workbook.save(caminho)


def test_ler_produz_dicts_com_as_colunas_do_cabecalho(tmp_path):
    caminho = tmp_path / "dados.xlsx"
    _escrever_xlsx(caminho, ["a", "b"], [{"a": "1", "b": "x"}, {"a": "2", "b": "y"}])

    linhas = list(ExcelReader(caminho).ler())

    assert linhas == [{"a": "1", "b": "x"}, {"a": "2", "b": "y"}]


def test_ler_converte_numero_inteiro_sem_sufixo_decimal(tmp_path):
    """openpyxl lê uma célula numérica como float (5.0); sem a
    normalização, isso quebraria int('5.0') nos Conversores -- o
    mesmo dado via CSV chegaria como a string '5'."""
    caminho = tmp_path / "dados.xlsx"
    workbook = Workbook()
    planilha = workbook.active
    planilha.append(["quantidade"])
    planilha.append([5])  # openpyxl vai armazenar/ler isso como 5.0
    workbook.save(caminho)

    linhas = list(ExcelReader(caminho).ler())

    assert linhas == [{"quantidade": "5"}]


def test_ler_ignora_linhas_completamente_vazias(tmp_path):
    caminho = tmp_path / "dados.xlsx"
    workbook = Workbook()
    planilha = workbook.active
    planilha.append(["a"])
    planilha.append(["1"])
    planilha.append([None])
    planilha.append(["2"])
    workbook.save(caminho)

    linhas = list(ExcelReader(caminho).ler())

    assert linhas == [{"a": "1"}, {"a": "2"}]


def test_ler_celula_vazia_vira_string_vazia(tmp_path):
    caminho = tmp_path / "dados.xlsx"
    _escrever_xlsx(caminho, ["a", "b"], [{"a": "1", "b": None}])

    linhas = list(ExcelReader(caminho).ler())

    assert linhas == [{"a": "1", "b": ""}]


def test_total_estimado_conta_linhas_de_dado_sem_cabecalho(tmp_path):
    caminho = tmp_path / "dados.xlsx"
    _escrever_xlsx(caminho, ["a"], [{"a": "1"}, {"a": "2"}, {"a": "3"}])

    assert ExcelReader(caminho).total_estimado() == 3


def test_total_estimado_arquivo_inexistente_devolve_none(tmp_path):
    assert ExcelReader(tmp_path / "nao_existe.xlsx").total_estimado() is None


def test_validar_arquivo_inexistente(tmp_path):
    problemas = ExcelReader(tmp_path / "nao_existe.xlsx").validar()

    assert len(problemas) == 1
    assert "não encontrado" in problemas[0]


def test_validar_coluna_obrigatoria_ausente(tmp_path):
    caminho = tmp_path / "dados.xlsx"
    _escrever_xlsx(caminho, ["nome"], [{"nome": "a"}])

    problemas = ExcelReader(caminho, colunas_obrigatorias=["nome", "inep"]).validar()

    assert len(problemas) == 1
    assert "inep" in problemas[0]


def test_validar_sem_problemas_quando_colunas_presentes(tmp_path):
    caminho = tmp_path / "dados.xlsx"
    _escrever_xlsx(caminho, ["nome", "inep"], [{"nome": "a", "inep": "12345678"}])

    problemas = ExcelReader(caminho, colunas_obrigatorias=["nome", "inep"]).validar()

    assert problemas == []


def test_le_aba_especifica_por_nome(tmp_path):
    caminho = tmp_path / "dados.xlsx"
    workbook = Workbook()
    workbook.active.title = "Outra"
    workbook.active.append(["x"])
    workbook.active.append(["ignorar"])
    planilha_certa = workbook.create_sheet("Dados")
    planilha_certa.append(["a"])
    planilha_certa.append(["1"])
    workbook.save(caminho)

    linhas = list(ExcelReader(caminho, aba="Dados").ler())

    assert linhas == [{"a": "1"}]


def test_validar_aba_inexistente(tmp_path):
    caminho = tmp_path / "dados.xlsx"
    _escrever_xlsx(caminho, ["a"], [{"a": "1"}])

    problemas = ExcelReader(caminho, aba="NaoExiste").validar()

    assert len(problemas) == 1
    assert "NaoExiste" in problemas[0]
