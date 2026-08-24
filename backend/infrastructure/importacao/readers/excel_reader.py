"""
ExcelReader: implementação concreta de Reader para arquivos .xlsx.

Prova de que o desacoplamento funciona (ver docs/importacao.md, seção
16): nenhuma linha de importacao/pipeline.py, importacao/mappers/ ou
scripts/importar_*.py precisou mudar pra isso existir. Só esta classe
sabe o que é um .xlsx.
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import Any, Iterator

from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet


class ExcelReader:
    """
    Lê um arquivo .xlsx linha a linha.

    `load_workbook(..., read_only=True)` do openpyxl é, ele mesmo,
    baseado em streaming por baixo dos panos (usa um parser XML
    incremental, não carrega a planilha inteira na árvore DOM) — a
    mesma propriedade de "nunca materializar o arquivo inteiro em
    memória" do CsvReader se mantém.

    Toda célula é convertida pra `str` antes de virar uma LinhaBruta
    (ver `_para_texto`), pro Mapper e os Conversores tratarem uma
    linha de Excel exatamente como tratam uma linha de CSV, sem saber
    a diferença.

    Parameters
    ----------
    caminho:
        Caminho do arquivo .xlsx.
    colunas_obrigatorias:
        Ver CsvReader — mesmo papel, mesma validação.
    aba:
        Nome da planilha a ler. None usa a planilha ativa (a primeira
        por padrão) — suficiente pra a maioria dos arquivos reais,
        que têm uma aba só de dados.
    """

    def __init__(
        self,
        caminho: str | Path,
        colunas_obrigatorias: list[str] | None = None,
        aba: str | None = None,
    ) -> None:
        self._caminho = Path(caminho)
        self._colunas_obrigatorias = colunas_obrigatorias or []
        self._aba = aba

    def validar(self) -> list[str]:
        if not self._caminho.exists():
            return [f"Arquivo não encontrado: {self._caminho}"]

        try:
            workbook = load_workbook(self._caminho, read_only=True)
        except Exception as excecao:
            return [f"Não foi possível abrir o arquivo Excel: {excecao}"]

        try:
            planilha = self._selecionar_planilha(workbook)
            if planilha is None:
                return [
                    f"Aba '{self._aba}' não encontrada. "
                    f"Abas disponíveis: {', '.join(workbook.sheetnames)}"
                ]

            colunas_presentes = set(self._ler_cabecalho(planilha))
            faltando = [
                c for c in self._colunas_obrigatorias if c not in colunas_presentes
            ]
            if faltando:
                return [
                    f"Coluna(s) obrigatória(s) ausente(s) no cabeçalho: "
                    f"{', '.join(faltando)}"
                ]
            return []
        finally:
            workbook.close()

    def ler(self) -> Iterator[dict[str, str]]:
        workbook = load_workbook(self._caminho, read_only=True)
        try:
            planilha = self._selecionar_planilha(workbook)
            if planilha is None:
                return

            linhas = planilha.iter_rows(values_only=True)
            cabecalho_bruto = next(linhas, None)
            if cabecalho_bruto is None:
                return
            cabecalho = [self._para_texto(c) for c in cabecalho_bruto]

            for linha in linhas:
                if all(valor is None for valor in linha):
                    # comum no fim de planilhas exportadas de outros
                    # sistemas: linhas em branco antes do fim real dos
                    # dados. Ignoradas, não viram uma LinhaBruta vazia.
                    continue
                yield {
                    coluna: self._para_texto(valor)
                    for coluna, valor in zip(cabecalho, linha)
                }
        finally:
            workbook.close()

    def total_estimado(self) -> int | None:
        if not self._caminho.exists():
            return None
        try:
            workbook = load_workbook(self._caminho, read_only=True)
        except Exception:
            return None
        try:
            planilha = self._selecionar_planilha(workbook)
            if planilha is None or planilha.max_row is None:
                return None
            return max(planilha.max_row - 1, 0)
        finally:
            workbook.close()

    def _selecionar_planilha(self, workbook: Any) -> Worksheet | None:
        if self._aba is not None:
            return workbook[self._aba] if self._aba in workbook.sheetnames else None
        return workbook.active

    @classmethod
    def _ler_cabecalho(cls, planilha: Worksheet) -> list[str]:
        primeira_linha = next(planilha.iter_rows(values_only=True), ())
        return [cls._para_texto(c) for c in primeira_linha]

    @staticmethod
    def _para_texto(valor: object) -> str:
        """
        Normaliza uma célula pra string, do jeito mais próximo
        possível do que csv.DictReader já entregaria pro mesmo dado
        digitado num CSV.
        """
        if valor is None:
            return ""
        if isinstance(valor, bool):
            return str(valor)
        if isinstance(valor, float) and valor.is_integer():
            # openpyxl lê a célula "5" como 5.0 (float); um CSV com
            # "5" chegaria como a string "5" — sem isso, o mesmo dado
            # produziria KitAluno=5 via CSV mas uma string "5.0" via
            # Excel, quebrando int("5.0").
            return str(int(valor))
        if isinstance(valor, (dt.datetime, dt.date)):
            return valor.isoformat()
        return str(valor)
