"""
Mapper de Escola — resolve dre_id a partir de dre_id direto ou
dre_nome, buscando entre as DREs já cadastradas no banco.
"""

from __future__ import annotations

from domain.repositories import DreRepository
from domain.value_objects import Nome
from application.use_cases.escola import CriarEscolaInput
from ..conversores import para_texto_opcional


class EscolaMapper:
    """
    Colunas esperadas: inep, nome, tipo, municipio (obrigatórias),
    endereco (opcional), e dre_id OU dre_nome (pelo menos uma).

    Depende de DreRepository só para resolver dre_nome -> dre_id —
    é a mesma ideia de resolver_dre_id que já existia em
    scripts/importar_escolas.py, só que como método de uma classe
    injetável em vez de função solta.
    """

    COLUNAS_OBRIGATORIAS = ["inep", "nome", "tipo", "municipio"]

    def __init__(self, repo_dre: DreRepository) -> None:
        self._repo_dre = repo_dre

    def mapear(self, linha: dict[str, str]) -> CriarEscolaInput:
        return CriarEscolaInput(
            inep=linha["inep"].strip(),
            nome=linha["nome"].strip(),
            tipo=linha["tipo"].strip().upper(),
            municipio=linha["municipio"].strip(),
            dre_id=self._resolver_dre_id(linha),
            endereco=para_texto_opcional(linha.get("endereco")),
        )

    def _resolver_dre_id(self, linha: dict[str, str]) -> int:
        dre_id_bruto = (linha.get("dre_id") or "").strip()
        if dre_id_bruto:
            return int(dre_id_bruto)

        nome = (linha.get("dre_nome") or "").strip()
        if not nome:
            raise ValueError("Linha não informou nem dre_id nem dre_nome.")

        encontradas = self._repo_dre.buscar_por_nome(Nome(nome))

        if not encontradas:
            raise ValueError(f"DRE com nome '{nome}' não encontrada.")
        if len(encontradas) > 1:
            raise ValueError(
                f"Mais de uma DRE encontrada com o nome '{nome}' "
                f"({len(encontradas)}) — use dre_id para desambiguar."
            )

        dre_id = encontradas[0].id
        if dre_id is None:
            raise ValueError(f"DRE com nome '{nome}' não possui id persistido.")
        return dre_id
