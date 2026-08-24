"""
Testes de importacao.readers.factory.criar_reader.
"""

from __future__ import annotations

from backend.infrastructure.importacao.readers import CsvReader, ExcelReader, criar_reader


def test_xlsx_devolve_excel_reader():
    assert isinstance(criar_reader("dados.xlsx"), ExcelReader)


def test_xlsm_devolve_excel_reader():
    assert isinstance(criar_reader("dados.xlsm"), ExcelReader)


def test_csv_devolve_csv_reader():
    assert isinstance(criar_reader("dados.csv"), CsvReader)


def test_extensao_desconhecida_devolve_csv_reader():
    """CSV é o padrão histórico do projeto -- qualquer coisa que não
    seja reconhecidamente Excel cai nele, em vez de levantar erro
    aqui (o próprio Reader.validar() reprova um arquivo ilegível)."""
    assert isinstance(criar_reader("dados.txt"), CsvReader)


def test_extensao_maiuscula_tambem_e_reconhecida():
    assert isinstance(criar_reader("dados.XLSX"), ExcelReader)


def test_repassa_colunas_obrigatorias(tmp_path):
    caminho = tmp_path / "dados.csv"
    caminho.write_text("nome\na\n", encoding="utf-8")

    reader = criar_reader(caminho, colunas_obrigatorias=["nome", "inep"])

    problemas = reader.validar()
    assert "inep" in problemas[0]
