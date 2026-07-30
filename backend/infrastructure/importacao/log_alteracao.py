"""
Log de alterações: registra o que mudou quando uma importação
ATUALIZA (em vez de criar) uma entidade já existente.

Estado atual do projeto: nenhum dos Use Cases de importação faz
update — a Fase 4 do roadmap é só criação ("Importação Inicial"). O
Pipeline já aceita essa peça pronta para o dia em que existir
reimportação incremental (ex.: reimportar um CSV corrigido e
atualizar, não duplicar, os registros que já existem) — mas hoje
`LogAlteracao` fica sem nenhum registro em qualquer importador atual,
porque nenhum Mapper/Use Case hoje distingue "criar" de "atualizar".
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class MudancaCampo:
    campo: str
    valor_antigo: Any
    valor_novo: Any


@dataclass(frozen=True)
class RegistroAlteracao:
    entidade: str
    identificador: int
    mudancas: list[MudancaCampo]
    ocorrido_em: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class LogAlteracao:
    """Acumula RegistroAlteracao em memória durante uma execução do
    Pipeline e sabe exportar tudo pra CSV ao final."""

    def __init__(self) -> None:
        self._registros: list[RegistroAlteracao] = []

    def registrar(
        self, entidade: str, identificador: int, mudancas: list[MudancaCampo]
    ) -> None:
        """Não grava nada se a lista de mudanças vier vazia — uma
        linha reimportada idêntica à existente não é uma alteração."""
        if not mudancas:
            return
        self._registros.append(RegistroAlteracao(entidade, identificador, mudancas))

    @property
    def registros(self) -> list[RegistroAlteracao]:
        return list(self._registros)

    def exportar_csv(self, caminho: str | Path) -> None:
        if not self._registros:
            return

        with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(
                ["entidade", "id", "campo", "valor_antigo", "valor_novo", "ocorrido_em"]
            )
            for registro in self._registros:
                for mudanca in registro.mudancas:
                    escritor.writerow(
                        [
                            registro.entidade,
                            registro.identificador,
                            mudanca.campo,
                            mudanca.valor_antigo,
                            mudanca.valor_novo,
                            registro.ocorrido_em.isoformat(),
                        ]
                    )
