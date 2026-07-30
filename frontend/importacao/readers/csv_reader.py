"""
CsvReader: implementação concreta de Reader para arquivos CSV.

É a ÚNICA peça deste módulo que sabe o que é um "CSV" — nenhum outro
arquivo do pacote `importacao` (pipeline, protocolos, mappers) importa
o módulo `csv`. Isso é o que torna trocar a fonte por Excel, Google
Sheets ou uma API no futuro uma questão de escrever uma nova classe
que satisfaça o Protocol Reader, sem tocar no Pipeline nem nos
Mappers — ver `docs/importacao.md` para o exemplo de ExcelReader.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterator


class CsvReader:
    """
    Lê um CSV linha a linha (streaming via yield) — nunca materializa
    o arquivo inteiro em memória, então funciona igual para um CSV de
    10 linhas ou de 500 mil.

    Parameters
    ----------
    caminho:
        Caminho do arquivo CSV.
    colunas_obrigatorias:
        Nomes de coluna que DEVEM existir no cabeçalho. Usado só por
        `validar()`, pra falhar rápido (antes de ler qualquer linha)
        se o arquivo não tiver o formato esperado — é o passo
        "Validação do arquivo" do pipeline, antes do Reader começar a
        de fato produzir linhas.
    encoding:
        Codificação do arquivo. Planilhas exportadas do Excel no
        Windows frequentemente vêm em "latin-1"/"cp1252", não utf-8.
    """

    def __init__(
        self,
        caminho: str | Path,
        colunas_obrigatorias: list[str] | None = None,
        encoding: str = "utf-8",
    ) -> None:
        self._caminho = Path(caminho)
        self._colunas_obrigatorias = colunas_obrigatorias or []
        self._encoding = encoding

    def validar(self) -> list[str]:
        problemas: list[str] = []

        if not self._caminho.exists():
            problemas.append(f"Arquivo não encontrado: {self._caminho}")
            return problemas  # sem arquivo, nenhuma checagem abaixo faz sentido

        with open(self._caminho, encoding=self._encoding, newline="") as arquivo:
            leitor = csv.DictReader(arquivo)
            colunas_presentes = set(leitor.fieldnames or [])

        faltando = [c for c in self._colunas_obrigatorias if c not in colunas_presentes]
        if faltando:
            problemas.append(
                f"Coluna(s) obrigatória(s) ausente(s) no cabeçalho: {', '.join(faltando)}"
            )

        return problemas

    def ler(self) -> Iterator[dict[str, str]]:
        with open(self._caminho, encoding=self._encoding, newline="") as arquivo:
            leitor = csv.DictReader(arquivo)
            yield from leitor

    def total_estimado(self) -> int | None:
        """
        Conta linhas de dado (exclui cabeçalho) com uma pré-passada
        O(n) em tempo mas O(1) em memória — soma newlines, não guarda
        conteúdo. Serve só pra dar um total ao ProgressTracker; se o
        arquivo não existir aqui, devolve None em vez de levantar (o
        Pipeline já vai ter interrompido em validar() antes de chegar
        aqui de qualquer forma).
        """
        if not self._caminho.exists():
            return None
        with open(self._caminho, encoding=self._encoding, newline="") as arquivo:
            total_linhas = sum(1 for _ in arquivo)
        return max(total_linhas - 1, 0)
