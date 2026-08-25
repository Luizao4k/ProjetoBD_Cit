"""
Regras de negocio para o nome 
"""
from dataclasses import dataclass
from unicodedata import normalize

from backend.shared.exceptions import NomeInvalidoError
from .. import MAX_LEN


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

        if len(valor) > MAX_LEN:
            raise NomeInvalidoError(
                f"Nome deve possuir no máximo {MAX_LEN} caracteres."
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
