"""
Mapper de Starlink — resolve escola_id a partir de escola_id direto
ou escola_inep.
"""

from __future__ import annotations

from domain.repositories import EscolaRepository
from application.use_cases.starlink import CriarStarlinkInput
from ..resolvedores import resolver_escola_id


class StarlinkMapper:
    """
    Colunas esperadas: designacao (obrigatória), e escola_id OU
    escola_inep (pelo menos uma).

    Diferente de Diretor/CEMEP/Chromebook, uma escola PODE ter várias
    designações de Starlink — não há restrição de unicidade de
    escola_id no schema, então múltiplas linhas para a mesma escola
    são válidas.
    """

    COLUNAS_OBRIGATORIAS = ["designacao"]

    def __init__(self, repo_escola: EscolaRepository) -> None:
        self._repo_escola = repo_escola

    def mapear(self, linha: dict[str, str]) -> CriarStarlinkInput:
        return CriarStarlinkInput(
            escola_id=resolver_escola_id(linha, self._repo_escola),
            designacao=linha["designacao"].strip(),
        )
