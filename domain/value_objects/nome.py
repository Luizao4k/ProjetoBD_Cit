"""
Regras de negocio para o nome 
"""
from dataclasses import dataclass
from unicodedata import normalize

from domain.constantes import MAX_NOME_LEN
from shared.exceptions import NomeInvalidoError


@dataclass(frozen=True)
class Nome:
    """
    Value_Object com validação
    """
    valor: str

    def __post_init__(self) -> None:
        valor = self.valor.strip()

        if not valor:
            raise NomeInvalidoError("Nome não pode ser vazio.")

        valor = self._remover_acentos(valor).upper()

        if len(valor) > MAX_NOME_LEN:
            raise NomeInvalidoError(
                f"Nome deve possuir no máximo {MAX_NOME_LEN} caracteres."
            )

        object.__setattr__(self, "valor", valor)

    @staticmethod
    def _remover_acentos(texto: str) -> str:
        return (
            normalize("NFKD", texto)
            .encode("ASCII", "ignore")
            .decode("ASCII")
        )

    def __str__(self) -> str:
        return self.valor
