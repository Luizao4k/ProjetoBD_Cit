"""
Mapper de Turma CEMEP.
"""

from __future__ import annotations

from backend.application.use_cases.turma_cemep import CriarTurmaCemepInput


class TurmaCemepMapper:
    """
    Colunas esperadas: nome_turma, responsavel_id (ambas
    obrigatórias).

    Diferente dos outros Mappers, aqui só aceito responsavel_id
    direto — de propósito, não por esquecimento. ResponsavelRepository
    não expõe nenhuma busca por nome (só buscar_por_id e
    buscar_por_cemep, que devolve uma lista). Resolver por nome
    exigiria encadear escola_inep -> escola_id -> cemep_id ->
    lista de responsáveis -> filtrar por nome em Python, sem garantia
    de nome único dentro do mesmo CEMEP — uma ambiguidade silenciosa
    que prefiro não introduzir. Se isso fizer falta na prática, dá
    pra adicionar depois (ver docs/importacao.md).

    Um responsável pode ter várias turmas (1:N) — não há restrição de
    unicidade de responsavel_id no schema.
    """

    COLUNAS_OBRIGATORIAS = ["nome_turma", "responsavel_id"]

    def mapear(self, linha: dict[str, str]) -> CriarTurmaCemepInput:
        return CriarTurmaCemepInput(
            responsavel_id=int(linha["responsavel_id"].strip()),
            nome_turma=linha["nome_turma"].strip(),
        )
