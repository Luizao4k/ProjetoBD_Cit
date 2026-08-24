"""
Mapper de Responsável — resolve cemep_id a partir de cemep_id direto
ou escola_inep (Cemep não tem nome próprio, só existe em função da
escola a que pertence).
"""

from __future__ import annotations

from backend.domain.repositories import CemepRepository, EscolaRepository
from backend.application.use_cases.responsavel import CriarResponsavelInput
from backend.infrastructure.importacao.resolvedores import resolver_cemep_id


class ResponsavelMapper:
    """
    Colunas esperadas: nome (obrigatória), e cemep_id OU escola_inep
    (pelo menos uma).

    Um CEMEP pode ter vários responsáveis (1:N) — não há restrição de
    unicidade de cemep_id no schema.
    """

    COLUNAS_OBRIGATORIAS = ["nome"]

    def __init__(self, repo_cemep: CemepRepository, repo_escola: EscolaRepository) -> None:
        self._repo_cemep = repo_cemep
        self._repo_escola = repo_escola

    def mapear(self, linha: dict[str, str]) -> CriarResponsavelInput:
        return CriarResponsavelInput(
            cemep_id=resolver_cemep_id(linha, self._repo_cemep, self._repo_escola),
            nome=linha["nome"].strip(),
        )
