"""
Utilitário genérico de importação em lote.

Usado por scripts como importar_escolas.py. A ideia central: uma linha
ruim nunca derruba o lote inteiro. Ela é registrada com o motivo da
falha e a importação segue para a próxima linha — quem rodou o
importador decide depois se corrige e reimporta só as que falharam.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, TypeVar

EntradaT = TypeVar("EntradaT")
SaidaT = TypeVar("SaidaT")


@dataclass
class LinhaFalha:
    """Uma linha que não pôde ser importada, com o motivo."""

    numero_linha: int
    dados_originais: dict[str, Any]
    tipo_erro: str
    motivo: str


@dataclass
class ResultadoImportacao:
    """Resumo de uma importação em lote."""

    sucesso: list[Any] = field(default_factory=list)
    falhas: list[LinhaFalha] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.sucesso) + len(self.falhas)

    def resumo(self) -> str:
        return (
            f"{len(self.sucesso)}/{self.total} linha(s) importada(s) com sucesso, "
            f"{len(self.falhas)} falha(s)."
        )


def importar_em_lote(
    linhas: list[dict[str, Any]],
    *,
    montar_entrada: Callable[[dict[str, Any]], EntradaT],
    executar: Callable[[EntradaT], SaidaT],
) -> ResultadoImportacao:
    """
    Executa `executar(montar_entrada(linha))` para cada linha de `linhas`.

    Qualquer exceção — Value Object inválido, entidade relacionada não
    encontrada, registro duplicado, falha de persistência, ou até um
    erro de programação como KeyError numa coluna faltante — é
    capturada por linha. A linha entra em `resultado.falhas` junto com
    o motivo, e o laço segue pra próxima. Nada propaga pra fora e
    interrompe o lote; essa é a garantia deste utilitário.

    Args:
        linhas: uma linha por dict (ex: cada linha de um CSV já lido).
        montar_entrada: converte a linha crua no Input DTO do caso de
            uso (aqui é o lugar certo pra resolver ids por nome, etc).
        executar: recebe o Input DTO e roda o caso de uso.
    """
    resultado = ResultadoImportacao()

    for numero, linha in enumerate(linhas, start=1):
        try:
            entrada = montar_entrada(linha)
            saida = executar(entrada)
            resultado.sucesso.append(saida)

        except Exception as exc:  # noqa: BLE001 — intencional, ver docstring
            resultado.falhas.append(
                LinhaFalha(
                    numero_linha=numero,
                    dados_originais=linha,
                    tipo_erro=type(exc).__name__,
                    motivo=str(exc),
                )
            )

    return resultado


def ler_csv(caminho: str | Path) -> list[dict[str, str]]:
    """
    Lê um CSV com cabeçalho e devolve uma linha por dict.
    Encoding utf-8, delimitador vírgula (padrão de planilhas exportadas
    do Excel/Google Sheets salvas como CSV).
    """
    with open(caminho, encoding="utf-8-sig", newline="") as arquivo:
        return list(csv.DictReader(arquivo))


def exportar_falhas_csv(resultado: ResultadoImportacao, caminho: str | Path) -> None:
    """
    Grava as linhas que falharam num CSV — colunas originais da linha
    mais `numero_linha`, `tipo_erro` e `motivo` no final. Pensado pra
    ser aberto e corrigido em planilha e reimportado depois.

    Não faz nada se não houver falhas (não sobrescreve um CSV antigo
    com um arquivo vazio).
    """
    if not resultado.falhas:
        return

    colunas_originais = list(resultado.falhas[0].dados_originais.keys())
    colunas = colunas_originais + ["numero_linha", "tipo_erro", "motivo"]

    with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()
        for falha in resultado.falhas:
            escritor.writerow(
                {
                    **falha.dados_originais,
                    "numero_linha": falha.numero_linha,
                    "tipo_erro": falha.tipo_erro,
                    "motivo": falha.motivo,
                }
            )
