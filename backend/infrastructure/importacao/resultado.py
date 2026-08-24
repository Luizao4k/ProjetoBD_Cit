"""
Resultado agregado de uma execução do ImportadorPipeline.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Generic, TypeVar

from backend.infrastructure.importacao.erro import ErroImportacao

TSaida = TypeVar("TSaida")


@dataclass
class ResultadoImportacao(Generic[TSaida]):
    """
    Genérico na saída do Use Case (TSaida) — o Pipeline de Escola
    devolve ResultadoImportacao[EscolaOutput], o de DRE devolve
    ResultadoImportacao[DreOutput], mas a classe em si é escrita uma
    única vez.
    """

    sucessos: list[TSaida] = field(default_factory=list)
    erros: list[ErroImportacao] = field(default_factory=list)

    def registrar_sucesso(self, saida: TSaida) -> None:
        self.sucessos.append(saida)

    def registrar_erro(self, erro: ErroImportacao) -> None:
        self.erros.append(erro)

    @property
    def total_processado(self) -> int:
        return len(self.sucessos) + len(self.erros)

    @property
    def taxa_sucesso(self) -> float:
        if self.total_processado == 0:
            return 0.0
        return len(self.sucessos) / self.total_processado

    def resumo(self) -> str:
        return (
            f"{len(self.sucessos)} registro(s) importado(s) com sucesso, "
            f"{len(self.erros)} falha(s) "
            f"({self.taxa_sucesso:.1%} de sucesso, "
            f"{self.total_processado} linha(s) processada(s) no total)."
        )

    def exportar_falhas_csv(self, caminho: str | Path) -> None:
        """
        Grava as linhas que falharam num CSV no MESMO formato de
        entrada (colunas originais) mais numero_linha/tipo_erro/motivo
        ao final — pensado para abrir em planilha, corrigir e
        reimportar como um novo arquivo de entrada. Não escreve nada
        se não houver falhas (não sobrescreve um relatório antigo com
        um arquivo vazio).
        """
        if not self.erros:
            return

        colunas_originais = list(self.erros[0].dados_originais.keys())
        colunas = colunas_originais + ["numero_linha", "tipo_erro", "motivo"]

        with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=colunas)
            escritor.writeheader()
            for erro in self.erros:
                escritor.writerow(erro.linha_relatorio())

    def relatorio_por_tipo_erro(self) -> dict[str, int]:
        """Contagem de falhas agrupadas por tipo de exceção — útil
        pra um resumo tipo 'InepJaCadastradoError: 3, KeyError: 1'."""
        contagem: dict[str, int] = {}
        for erro in self.erros:
            contagem[erro.tipo_erro] = contagem.get(erro.tipo_erro, 0) + 1
        return contagem
