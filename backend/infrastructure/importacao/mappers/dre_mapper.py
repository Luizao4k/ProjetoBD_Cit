"""
Mapper de DRE — o mais simples de todos: CriarDreInput não tem
nenhuma chave estrangeira pra resolver.
"""

from __future__ import annotations

from backend.application.use_cases.dre import CriarDreInput
from backend.infrastructure.importacao.conversores import para_texto_opcional


class DreMapper:
    """Colunas esperadas: nome (obrigatória), telefone (opcional)."""

    COLUNAS_OBRIGATORIAS = ["nome"]

    def mapear(self, linha: dict[str, str]) -> CriarDreInput:
        return CriarDreInput(
            nome=linha["nome"].strip(),
            telefone=para_texto_opcional(linha.get("telefone")),
        )
