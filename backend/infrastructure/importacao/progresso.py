"""
Rastreamento de progresso da importação.
"""

from __future__ import annotations

import sys
from typing import Protocol, runtime_checkable

from .resultado import ResultadoImportacao


@runtime_checkable
class ProgressTracker(Protocol):
    """
    Interface mínima pra qualquer forma de exibir progresso — console,
    barra gráfica, callback pra uma UI web, log estruturado. O
    Pipeline não sabe (nem precisa saber) qual está sendo usada.
    """

    def atualizar(self, processados: int, total: int | None) -> None: ...

    def finalizar(self, resultado: ResultadoImportacao) -> None: ...


class ProgressTrackerConsole:
    """
    Implementação padrão: imprime em stderr (não polui uma saída que
    porventura seja redirecionada/parseada) a cada `intervalo` linhas
    — pra um arquivo de 50 mil linhas não produzir 50 mil prints.
    """

    def __init__(self, intervalo: int = 500) -> None:
        self._intervalo = intervalo

    def atualizar(self, processados: int, total: int | None) -> None:
        if processados % self._intervalo != 0:
            return
        self._imprimir(processados, total)

    def finalizar(self, resultado: ResultadoImportacao) -> None:
        print(file=sys.stderr)
        print(resultado.resumo())

    def _imprimir(self, processados: int, total: int | None) -> None:
        if total:
            print(
                f"\r  processando... {processados}/{total} ({processados / total:.1%})",
                end="",
                file=sys.stderr,
            )
        else:
            print(f"\r  processando... {processados} linha(s)", end="", file=sys.stderr)


class ProgressTrackerSilencioso:
    """Não imprime nada — útil em testes, pra não poluir a saída do
    pytest com barras de progresso."""

    def atualizar(self, processados: int, total: int | None) -> None:
        pass

    def finalizar(self, resultado: ResultadoImportacao) -> None:
        pass
