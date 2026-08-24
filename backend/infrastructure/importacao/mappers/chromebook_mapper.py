"""
Mapper de Chromebook — resolve escola_id a partir de escola_id direto
ou escola_inep, e converte kit_aluno/kit_professor pra int.
"""

from __future__ import annotations

from backend.domain.repositories import EscolaRepository
from backend.application.use_cases.chromebook import CriarChromebookInput
from backend.infrastructure.importacao.conversores import para_inteiro_opcional
from backend.infrastructure.importacao.resolvedores import resolver_escola_id


class ChromebookMapper:
    """
    Colunas esperadas: kit_aluno e kit_professor (opcionais, mas se
    vierem precisam ser inteiros — CriarChromebookInput espera `int`,
    não `str`, então a conversão acontece aqui, não dentro do Value
    Object Quantidade), e escola_id OU escola_inep (pelo menos uma).

    Cada escola só pode ter um registro de Chromebook (1:1 no schema)
    — uma segunda linha pra mesma escola vira
    EscolaJaPossuiChromebookError, capturado normalmente pelo
    Pipeline como falha da linha.
    """

    COLUNAS_OBRIGATORIAS: list[str] = []

    def __init__(self, repo_escola: EscolaRepository) -> None:
        self._repo_escola = repo_escola

    def mapear(self, linha: dict[str, str]) -> CriarChromebookInput:
        return CriarChromebookInput(
            escola_id=resolver_escola_id(linha, self._repo_escola),
            kit_aluno=para_inteiro_opcional(linha.get("kit_aluno")),
            kit_professor=para_inteiro_opcional(linha.get("kit_professor")),
        )
