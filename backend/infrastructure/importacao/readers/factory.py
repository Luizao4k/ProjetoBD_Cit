"""
criar_reader: escolhe CsvReader ou ExcelReader pela extensão do
arquivo, para que cada scripts/importar_*.py aceite .csv e .xlsx sem
precisar saber qual dos dois está lendo.
"""

from __future__ import annotations

from pathlib import Path

from backend.infrastructure.importacao.protocolos import Reader
from backend.infrastructure.importacao.readers.csv_reader import CsvReader
from backend.infrastructure.importacao.readers.excel_reader import ExcelReader

_EXTENSOES_EXCEL = {".xlsx", ".xlsm"}


def criar_reader(
    caminho: str | Path,
    colunas_obrigatorias: list[str] | None = None,
) -> Reader:
    """
    .xlsx/.xlsm -> ExcelReader; qualquer outra extensão (.csv, sem
    extensão, etc.) -> CsvReader, que é o padrão histórico do
    projeto. Não inspeciona o conteúdo do arquivo, só o sufixo do
    nome — mais prova de que a fonte pode variar sem que o Pipeline,
    o Mapper ou o Use Case percebam qualquer diferença.
    """
    extensao = Path(caminho).suffix.lower()

    if extensao in _EXTENSOES_EXCEL:
        return ExcelReader(caminho, colunas_obrigatorias=colunas_obrigatorias)

    return CsvReader(caminho, colunas_obrigatorias=colunas_obrigatorias)
