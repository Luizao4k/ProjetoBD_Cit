"""
Mapper de CEMEP — resolve escola_id a partir de escola_id direto ou
escola_inep.
"""

from __future__ import annotations

from domain.repositories import EscolaRepository
from application.use_cases.cemep import CriarCemepInput
from infrastructure.importacao.conversores import para_texto_opcional
from infrastructure.importacao.resolvedores import resolver_escola_id


class CemepMapper:
    """
    Colunas esperadas: comentario (opcional), e escola_id OU
    escola_inep (pelo menos uma).

    Cada escola só pode ter um CEMEP (1:1 no schema) — uma segunda
    linha pra mesma escola vira EscolaJaPossuiCemepError, capturado
    normalmente pelo Pipeline como falha da linha.
    """

    COLUNAS_OBRIGATORIAS: list[str] = []

    def __init__(self, repo_escola: EscolaRepository) -> None:
        self._repo_escola = repo_escola

    def mapear(self, linha: dict[str, str]) -> CriarCemepInput:
        return CriarCemepInput(
            escola_id=resolver_escola_id(linha, self._repo_escola),
            comentario=para_texto_opcional(linha.get("comentario")),
        )
